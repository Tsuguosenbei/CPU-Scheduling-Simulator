"""Tkinter front end for the existing, independently testable scheduling engine."""
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from PIL import Image, ImageDraw, ImageFont, ImageTk
except ImportError:
    Image = ImageDraw = ImageFont = ImageTk = None

from scheduler import Process, validate_processes, fcfs, sjf, srtf, priority_scheduling
from calculations import metrics

ALGORITHMS = [('FCFS', fcfs), ('SJF', sjf), ('SRTF', srtf), ('Priority', priority_scheduling)]
COLORS = ['#2563eb', '#0d9488', '#d97706', '#7c3aed', '#be185d', '#0369a1']
NAVY = '#0f172a'
BLUE = '#2563eb'
BG = '#f1f5f9'
MUTED = '#64748b'


class RoundedButton(tk.Frame):
    """Antialiased rounded button; standard ttk fallback when Pillow is absent."""
    def __init__(self, parent, text, command, primary=False, width=150, height=38):
        parent_bg = parent.cget('bg')
        super().__init__(parent, bg=parent_bg, width=width, height=height)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.command = command
        self.primary = primary
        self.text = text
        self.width_px = width
        self.height_px = height
        self._images = {}
        if Image is None:
            style = 'Primary.TButton' if primary else 'TButton'
            self.control = ttk.Button(self, text=text, command=command, style=style)
            self.control.pack(fill='both', expand=True)
            return
        self.control = tk.Label(self, bg=parent_bg, bd=0, cursor='hand2',
                                takefocus=1, highlightthickness=0)
        self.control.pack(fill='both', expand=True)
        for state in ('normal', 'hover', 'pressed'):
            self._images[state] = self._make_image(state, parent_bg)
        self._show('normal')
        self.control.bind('<Enter>', lambda e: self._show('hover'))
        self.control.bind('<Leave>', lambda e: self._show('normal'))
        self.control.bind('<ButtonPress-1>', lambda e: self._show('pressed'))
        self.control.bind('<ButtonRelease-1>', self._release)
        self.control.bind('<Return>', lambda e: self.command())
        self.control.bind('<space>', lambda e: self.command())

    def _make_image(self, state, background):
        scale = 4
        w, h = self.width_px, self.height_px
        fill = ({'normal': '#2563eb', 'hover': '#1d4ed8', 'pressed': '#1e40af'}
                if self.primary else
                {'normal': '#e8eef8', 'hover': '#dbeafe', 'pressed': '#cbd5e1'})[state]
        img = Image.new('RGB', (w * scale, h * scale), background)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((1 * scale, 1 * scale,
                                (w - 2) * scale, (h - 2) * scale),
                               radius=9 * scale, fill=fill)
        font = None
        for path in ('C:/Windows/Fonts/segoeuib.ttf' if self.primary else 'C:/Windows/Fonts/segoeui.ttf',
                     '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
            try:
                font = ImageFont.truetype(path, 10 * scale)
                break
            except OSError:
                pass
        if font is None:
            font = ImageFont.load_default(size=10 * scale)
        draw.text((w * scale / 2, h * scale / 2), self.text,
                  font=font, fill='white' if self.primary else NAVY, anchor='mm')
        return ImageTk.PhotoImage(img.resize((w, h), Image.Resampling.LANCZOS))

    def _show(self, state):
        self.control.configure(image=self._images[state])

    def _release(self, event):
        self._show('hover')
        if 0 <= event.x < self.width_px and 0 <= event.y < self.height_px:
            self.command()


class RoundedField(tk.Frame):
    """Colored input card: label and entry share one rounded visual surface."""
    def __init__(self, parent, label):
        super().__init__(parent, bg='#eaf1fb', padx=12, pady=8)
        tk.Label(self, text=label, bg='#eaf1fb', fg='#475569',
                 font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.entry = tk.Entry(self, bg='#eaf1fb', fg=NAVY, insertbackground=NAVY,
                              relief='flat', highlightthickness=0, bd=0,
                              font=('Segoe UI', 11))
        self.entry.pack(fill='x', pady=(4, 1))


class SchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PT 101 | CPU Scheduling Studio')
        self.geometry('1250x850')
        self.minsize(950, 680)
        self.configure(bg=BG)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('App.TFrame', background=BG)
        self.style.configure('Card.TLabelframe', background='white', bordercolor='#dbe3ef', relief='solid')
        self.style.configure('Card.TLabelframe.Label', background=BG, foreground=NAVY,
                             font=('Segoe UI', 11, 'bold'))
        self.style.configure('TFrame', background='white')
        self.style.configure('TLabel', background='white', foreground=NAVY, font=('Segoe UI', 10))
        self.style.configure('TEntry', padding=7)
        self.style.configure('TButton', padding=(12, 8), font=('Segoe UI', 10))
        self.style.configure('Primary.TButton', background=BLUE, foreground='white',
                             font=('Segoe UI', 10, 'bold'), padding=(18, 9), borderwidth=0)
        self.style.map('Primary.TButton', background=[('active', '#1d4ed8'), ('pressed', '#1e40af')])
        self.style.configure('Treeview', rowheight=30, font=('Segoe UI', 10),
                             background='white', fieldbackground='white', foreground=NAVY,
                             bordercolor='#e2e8f0')
        self.style.map('Treeview', background=[('selected', '#dbeafe')],
                       foreground=[('selected', NAVY)])
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'),
                             background='#e8eef8', foreground=NAVY, padding=7)
        self.style.configure('TNotebook', background=BG, borderwidth=0)
        self.style.configure('TNotebook.Tab', padding=(20, 11), font=('Segoe UI', 10, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', 'white')],
                       foreground=[('selected', BLUE)])
        self.processes = []
        self.results = {}
        self._build()
        self.load_sample()

    def _build(self):
        header = tk.Frame(self, bg=NAVY, padx=24, pady=10)
        header.pack(fill='x')
        tk.Label(header, text='CPU SCHEDULING STUDIO', bg=NAVY, fg='white',
                 font=('Segoe UI', 19, 'bold')).pack(anchor='w')
        tk.Label(header, text='PT 101  /  PLATFORM TECHNOLOGIES     •     FCFS   •   SJF   •   SRTF   •   PRIORITY',
                 bg=NAVY, fg='#93c5fd', font=('Segoe UI', 10)).pack(anchor='w', pady=(2, 0))
        outer = ttk.Frame(self, padding=12, style='App.TFrame')
        outer.pack(fill='both', expand=True)
        inputs = ttk.LabelFrame(outer, text='  01  /  Process Workspace  ', padding=10,
                                style='Card.TLabelframe')
        inputs.pack(fill='x')
        form = tk.Frame(inputs, bg='white')
        form.pack(fill='x', pady=(0, 5))
        self.entries = {}
        for i, (field, label) in enumerate([('pid', 'Process ID'), ('at', 'Arrival Time'),
                                           ('bt', 'Burst Time'), ('priority', 'Priority  (1 = highest)')]):
            block = RoundedField(form, label)
            block.grid(row=0, column=i, sticky='ew', padx=(0, 10))
            self.entries[field] = block.entry
            form.columnconfigure(i, weight=1)
        RoundedButton(form, '+ Add Process', self.add_process, True, width=146, height=44).grid(
            row=0, column=4, padx=4, sticky='s')
        RoundedButton(form, 'Remove Selected', self.remove_selected, width=156, height=44).grid(
            row=0, column=5, padx=4, sticky='s')
        columns = ('pid', 'at', 'bt', 'priority')
        self.input_table = ttk.Treeview(inputs, columns=columns, show='headings', height=4,
                                        selectmode='extended')
        for col, heading in zip(columns, ['Process ID', 'Arrival Time', 'Burst Time', 'Priority']):
            self.input_table.heading(col, text=heading)
            self.input_table.column(col, width=140, anchor='center')
        self.input_table.pack(fill='x', pady=(7, 6))
        actions = tk.Frame(inputs, bg='white')
        actions.pack(fill='x')
        RoundedButton(actions, 'Load Sample', self.load_sample, width=125).pack(side='left', padx=(0, 8))
        RoundedButton(actions, 'Clear All', self.clear_all, width=110).pack(side='left')
        RoundedButton(actions, '▶  Run All Algorithms', self.run_all, True, width=215).pack(side='right')
        self.status = tk.StringVar(value='Ready. Enter processes or load sample data.')
        status_bar = tk.Frame(outer, bg='#e0eaff', padx=12, pady=6)
        status_bar.pack(fill='x', pady=(7, 7))
        tk.Label(status_bar, textvariable=self.status, bg='#e0eaff', fg='#1e40af',
                 font=('Segoe UI', 10)).pack(anchor='w')
        # Hide native tabs (their selected style shrinks on some Windows themes).
        # A fixed-height custom navigation bar supplies a persistent active outline.
        self.style.layout('Hidden.TNotebook.Tab', [])
        self.style.layout('Hidden.TNotebook', [('Notebook.client', {'sticky': 'nswe'})])
        self.tab_bar = tk.Frame(outer, bg=BG)
        self.tab_bar.pack(fill='x', pady=(2, 0))
        self.notebook = ttk.Notebook(outer, style='Hidden.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        self.tabs = {}
        for name, _ in ALGORITHMS:
            tab = ttk.Frame(self.notebook, padding=12)
            self.notebook.add(tab, text=name)
            self.tabs[name] = tab
        self.compare_tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.compare_tab, text='Comparison')
        self.nav_buttons = {}
        for name in [n for n, _ in ALGORITHMS] + ['Comparison']:
            btn = tk.Label(self.tab_bar, text=('★  ' if name == 'Comparison' else '') + name,
                           bg='#e2e8f0', fg=NAVY, font=('Segoe UI', 10, 'bold'),
                           padx=21, pady=12, cursor='hand2', highlightthickness=2,
                           highlightbackground=BG, highlightcolor=BLUE)
            btn.pack(side='left', padx=(0, 7))
            btn.bind('<Button-1>', lambda event, n=name: self._select_tab(n))
            self.nav_buttons[name] = btn
        self.notebook.bind('<<NotebookTabChanged>>', lambda e: self._update_nav())
        self._update_nav()
        self._empty_results()

    def _select_tab(self, name):
        self.notebook.select(self.compare_tab if name == 'Comparison' else self.tabs[name])
        self._update_nav()

    def _update_nav(self):
        selected = self.notebook.select()
        for name, button in self.nav_buttons.items():
            target = self.compare_tab if name == 'Comparison' else self.tabs[name]
            active = selected == str(target)
            button.configure(bg='#dbeafe' if active else '#e2e8f0',
                             fg='#1d4ed8' if active else NAVY,
                             highlightbackground=BLUE if active else BG)

    def _empty_results(self):
        for name, tab in self.tabs.items():
            self._clear(tab)
            ttk.Label(tab, text=f'{name}  /  Awaiting simulation',
                      font=('Segoe UI', 13, 'bold')).pack(anchor='w', pady=14)
            ttk.Label(tab, text='Click Run All Algorithms to generate a Gantt chart and process metrics.').pack(anchor='w')
        self._clear(self.compare_tab)
        ttk.Label(self.compare_tab, text='Algorithm Comparison  /  Awaiting simulation',
                  font=('Segoe UI', 13, 'bold')).pack(anchor='w', pady=14)
        ttk.Label(self.compare_tab, text='Run all algorithms to compare their average metrics.').pack(anchor='w')

    def _invalidate_results(self):
        self.results.clear()
        self._empty_results()

    def _refresh_inputs(self):
        self.input_table.delete(*self.input_table.get_children())
        for p in self.processes:
            self.input_table.insert('', 'end', values=(p.pid, p.arrival_time, p.burst_time, p.priority))

    def add_process(self):
        try:
            pid = self.entries['pid'].get().strip()
            p = Process(pid, int(self.entries['at'].get()), int(self.entries['bt'].get()),
                        int(self.entries['priority'].get()), len(self.processes))
            proposed = self.processes + [p]
            validate_processes(proposed)
        except ValueError as exc:
            messagebox.showerror('Invalid process', str(exc) if str(exc) and 'invalid literal' not in str(exc) else
                                 'Enter valid whole numbers for arrival, burst, and priority.')
            return
        self.processes.append(p)
        self._refresh_inputs()
        self._invalidate_results()
        for entry in self.entries.values():
            entry.delete(0, 'end')
        self.entries['pid'].focus_set()
        self.status.set(f'{len(self.processes)} process(es) entered. Run again to refresh results.')

    def remove_selected(self):
        selected = set(self.input_table.selection())
        if not selected:
            messagebox.showinfo('Select processes', 'Select one or more rows to remove.')
            return
        indices = {self.input_table.index(item) for item in selected}
        kept = [p for i, p in enumerate(self.processes) if i not in indices]
        self.processes = [Process(p.pid, p.arrival_time, p.burst_time, p.priority, i)
                          for i, p in enumerate(kept)]
        self._refresh_inputs()
        self._invalidate_results()
        self.status.set('Process list changed. Run again to update results.')

    def clear_all(self):
        self.processes.clear()
        self._refresh_inputs()
        self._invalidate_results()
        self.status.set('Process list cleared. Add processes to begin.')

    def load_sample(self):
        self.processes = [Process('P1', 0, 8, 3, 0), Process('P2', 1, 4, 1, 1),
                          Process('P3', 2, 2, 2, 2), Process('P4', 4, 1, 2, 3)]
        self._refresh_inputs()
        self._invalidate_results()
        self.status.set('Sample data loaded. Click Run All Algorithms.')

    def run_all(self):
        try:
            validate_processes(self.processes)
            self.results = {name: (fn(self.processes)) for name, fn in ALGORITHMS}
            for name, _ in ALGORITHMS:
                self._render_algorithm(self.tabs[name], self.results[name])
            self._render_comparison()
            self.notebook.select(self.compare_tab)
            self.status.set('✓ All four algorithms simulated. Comparison is ready; select any algorithm tab for details.')
        except (ValueError, KeyError) as exc:
            messagebox.showerror('Simulation error', str(exc))

    @staticmethod
    def _clear(frame):
        for child in frame.winfo_children():
            child.destroy()

    @staticmethod
    def _table(parent, columns, headings, rows, height=6):
        holder = ttk.Frame(parent)
        holder.pack(fill='x', pady=(4, 5))
        tree = ttk.Treeview(holder, columns=columns, show='headings', height=height)
        for col, label in zip(columns, headings):
            tree.heading(col, text=label)
            tree.column(col, anchor='center', width=90, minwidth=65)
        for row in rows:
            tree.insert('', 'end', values=row)
        tree.pack(side='left', fill='x', expand=True)
        if len(rows) > height:
            scrollbar = ttk.Scrollbar(holder, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side='right', fill='y')
        return tree

    def _render_algorithm(self, tab, result):
        self._clear(tab)
        rows, averages = metrics(self.processes, result)
        ttk.Label(tab, text=f'{result.algorithm}  /  Execution Timeline', font=('Segoe UI', 14, 'bold')).pack(anchor='w')
        ttk.Label(tab, text='Blue/colored blocks = execution; gray = idle. Times are shown at segment boundaries.').pack(anchor='w')
        canvas = tk.Canvas(tab, height=90, bg='white', highlightthickness=1, highlightbackground='#cbd5e1')
        canvas.pack(fill='x', pady=(5, 7))
        # Draw after geometry is known; redraw on resize.
        def draw(event=None):
            canvas.delete('all')
            width = max(canvas.winfo_width(), 300)
            segments = result.segments
            total = max(1, segments[-1].end)
            left, right = 35, width - 35
            scale = (right - left) / total
            colors = {p.pid: COLORS[i % len(COLORS)] for i, p in enumerate(self.processes)}
            for seg in segments:
                x1 = left + seg.start * scale
                x2 = left + seg.end * scale
                fill = '#94a3b8' if seg.pid == 'IDLE' else colors.get(seg.pid, '#64748b')
                canvas.create_rectangle(x1, 10, x2, 50, fill=fill, outline='white')
                if x2 - x1 > 23:
                    canvas.create_text((x1 + x2) / 2, 30, text=seg.pid, fill='white', font=('Segoe UI', 9, 'bold'))
                canvas.create_line(x1, 50, x1, 58, fill='#475569')
                canvas.create_text(x1, 72, text=str(seg.start), fill='#334155', font=('Segoe UI', 8))
            canvas.create_text(right, 72, text=str(segments[-1].end), fill='#334155', font=('Segoe UI', 8))
        canvas.bind('<Configure>', draw)
        timeline = '   |   '.join(f'{s.start} → {s.pid} → {s.end}' for s in result.segments)
        timeline_box = tk.Text(tab, height=1, wrap='word', bg='#eff6ff', fg='#1e3a8a',
                               relief='flat', padx=12, pady=5, font=('Consolas', 10))
        timeline_box.insert('1.0', 'TIMELINE    ' + timeline)
        timeline_box.configure(state='disabled')
        timeline_box.pack(fill='x', pady=(0, 6))
        ttk.Label(tab, text='Per-process Metrics', font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        cols = ('pid', 'at', 'bt', 'priority', 'ct', 'tat', 'wt', 'rt')
        self._table(tab, cols, ['PID', 'AT', 'BT', 'Priority', 'CT', 'TAT', 'WT', 'RT'],
                    [[r[c] for c in cols] for r in rows], height=min(7, max(3, len(rows))))
        self._metric_cards(tab, [('AVERAGE TURNAROUND', averages['tat']),
                                 ('AVERAGE WAITING', averages['wt']),
                                 ('AVERAGE RESPONSE', averages['rt'])])

    @staticmethod
    def _metric_cards(parent, values):
        cards = tk.Frame(parent, bg='white')
        cards.pack(fill='x', pady=(3, 2))
        for i, (label, value) in enumerate(values):
            card = tk.Frame(cards, bg='#eff6ff', padx=12, pady=3,
                            highlightbackground='#dbeafe', highlightthickness=1)
            card.grid(row=0, column=i, sticky='ew', padx=(0, 10) if i < len(values)-1 else 0)
            cards.columnconfigure(i, weight=1)
            tk.Label(card, text=label, bg='#eff6ff', fg=MUTED,
                     font=('Segoe UI', 9, 'bold')).pack(anchor='w')
            tk.Label(card, text=f'{value:.2f}', bg='#eff6ff', fg='#1d4ed8',
                     font=('Segoe UI', 16, 'bold')).pack(anchor='w')

    def _render_comparison(self):
        tab = self.compare_tab
        self._clear(tab)
        ttk.Label(tab, text='Algorithm Comparison  /  Performance Overview', font=('Segoe UI', 14, 'bold')).pack(anchor='w')
        ttk.Label(tab, text='Lower average turnaround, waiting, and response times are generally preferable for these metrics.').pack(anchor='w', pady=4)
        summary = [(name, metrics(self.processes, result)[1]) for name, result in self.results.items()]
        self._table(tab, ('algorithm', 'tat', 'wt', 'rt'),
                    ['Algorithm', 'Avg TAT', 'Avg WT', 'Avg RT'],
                    [(name, f"{avg['tat']:.2f}", f"{avg['wt']:.2f}", f"{avg['rt']:.2f}") for name, avg in summary],
                    height=4)
        for key, title in [('tat', 'Turnaround'), ('wt', 'Waiting'), ('rt', 'Response')]:
            best = min(avg[key] for _, avg in summary)
            winners = ', '.join(name for name, avg in summary if abs(avg[key] - best) < 1e-9)
            ttk.Label(tab, text=f'Lowest average {title} Time: {winners} ({best:.2f})',
                      font=('Segoe UI', 10)).pack(anchor='w', pady=5)
        ttk.Label(tab, text='Note: Different algorithms optimize different behaviors; a single metric does not determine universal superiority.',
                  wraplength=900, foreground='#475569').pack(anchor='w', pady=12)


if __name__ == '__main__':
    SchedulerApp().mainloop()
