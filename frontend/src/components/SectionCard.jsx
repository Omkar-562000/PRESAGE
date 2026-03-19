export function SectionCard({ title, subtitle, children, actions }) {
  return (
    <section className="rounded-[28px] border border-white/8 bg-panel/85 shadow-panel backdrop-blur">
      <div className="flex flex-col gap-3 border-b border-white/8 px-6 py-5 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="font-display text-2xl text-white">{title}</h2>
          {subtitle ? <p className="mt-1 text-sm text-steel">{subtitle}</p> : null}
        </div>
        {actions}
      </div>
      <div className="p-6">{children}</div>
    </section>
  );
}
