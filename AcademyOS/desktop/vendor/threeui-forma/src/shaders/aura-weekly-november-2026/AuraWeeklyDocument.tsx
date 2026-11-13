import type { CSSProperties } from "react";
export type AuraWeeklyDocumentProps = { className?: string; style?: CSSProperties };
export function AuraWeeklyDocument({ src, title, className = "", style }: AuraWeeklyDocumentProps & { src: string; title: string }) {
  return <div className={`threeui-background ${className}`} role="group" aria-label={title} style={{ position: "relative", overflow: "hidden", background: "#101114", pointerEvents: "auto", ...style }}>
    <iframe src={src} title={title} loading="lazy" sandbox="allow-scripts allow-forms" style={{ position: "absolute", inset: 0, width: "100%", height: "100%", border: 0 }} />
  </div>;
}
