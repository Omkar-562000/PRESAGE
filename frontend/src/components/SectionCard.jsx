export function SectionCard({ title, subtitle, children, actions }) {
  return (
    <section className="overflow-hidden rounded-[30px] border border-white/8 bg-panel/80 shadow-panel backdrop-blur animate-fade-rise">
      <div className="relative flex flex-col gap-3 border-b border-white/8 px-6 py-5 md:flex-row md:items-end md:justify-between">
        <div className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-sky/50 to-transparent" />
        <div>
          <p className="text-[10px] uppercase tracking-[0.34em] text-sky/80">Module View</p>
          <h2 className="mt-2 font-display text-[2rem] leading-none text-white">{title}</h2>
          {subtitle ? <p className="mt-2 max-w-2xl text-sm leading-6 text-steel">{subtitle}</p> : null}
        </div>
        {actions}
      </div>
      <div className="p-6">{children}</div>
    </section>
  );
}
