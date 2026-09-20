css_additions = """
/* === KrishokTech Task-First Decision Hub Refined Styles === */
.border-bone\\/80 { border-color: rgba(231, 223, 208, 0.8) !important; }
.border-bone\\/60 { border-color: rgba(231, 223, 208, 0.6) !important; }
.border-leaf\\/20 { border-color: rgba(47, 93, 58, 0.20) !important; }
.border-leaf\\/40 { border-color: rgba(47, 93, 58, 0.40) !important; }
.border-ochre\\/20 { border-color: rgba(200, 137, 60, 0.20) !important; }
.border-ochre\\/30 { border-color: rgba(200, 137, 60, 0.30) !important; }
.border-ochre\\/50 { border-color: rgba(200, 137, 60, 0.50) !important; }
.border-emerald-600\\/20 { border-color: rgba(5, 150, 105, 0.20) !important; }
.border-sky-600\\/20 { border-color: rgba(2, 132, 199, 0.20) !important; }
.border-sky-500\\/40 { border-color: rgba(14, 165, 233, 0.40) !important; }

.from-white\\/95 { --tw-gradient-from: rgba(255, 255, 255, 0.95) var(--tw-gradient-from-position); }
.to-leaf\\/\\[0\\.04\\] { --tw-gradient-to: rgba(47, 93, 58, 0.04) var(--tw-gradient-to-position); }
.to-emerald-600\\/\\[0\\.04\\] { --tw-gradient-to: rgba(5, 150, 105, 0.04) var(--tw-gradient-to-position); }
.to-ochre\\/\\[0\\.04\\] { --tw-gradient-to: rgba(200, 137, 60, 0.04) var(--tw-gradient-to-position); }
.to-sky-600\\/\\[0\\.04\\] { --tw-gradient-to: rgba(2, 132, 199, 0.04) var(--tw-gradient-to-position); }

.bg-paper-2\\/90 { background-color: rgba(242, 235, 220, 0.90) !important; }
.bg-white\\/90 { background-color: rgba(255, 255, 255, 0.90) !important; }
.bg-emerald-600\\/15 { background-color: rgba(5, 150, 105, 0.15) !important; }
.bg-sky-600\\/15 { background-color: rgba(2, 132, 199, 0.15) !important; }

.shadow-\\[0_4px_20px_-4px_rgba\\(52\\,39\\,23\\,0\\.06\\)\\] {
  box-shadow: 0 4px 20px -4px rgba(52, 39, 23, 0.06) !important;
}
.hover\\:shadow-\\[0_12px_32px_-6px_rgba\\(52\\,39\\,23\\,0\\.11\\)\\]:hover {
  box-shadow: 0 12px 32px -6px rgba(52, 39, 23, 0.11) !important;
}
.hover\\:shadow-\\[0_8px_30px_-6px_rgba\\(52\\,39\\,23\\,0\\.09\\)\\]:hover {
  box-shadow: 0 8px 30px -6px rgba(52, 39, 23, 0.09) !important;
}

.hover\\:border-leaf\\/40:hover { border-color: rgba(47, 93, 58, 0.40) !important; }
.hover\\:border-ochre\\/50:hover { border-color: rgba(200, 137, 60, 0.50) !important; }
.hover\\:border-sky-500\\/40:hover { border-color: rgba(14, 165, 233, 0.40) !important; }

.text-ink-soft\\/80 { color: rgba(51, 44, 37, 0.80) !important; }
.text-ink-soft\\/90 { color: rgba(51, 44, 37, 0.90) !important; }

.ring-4 { box-shadow: 0 0 0 4px var(--tw-ring-color, rgba(47,93,58,0.1)) !important; }
.ring-leaf\\/10 { --tw-ring-color: rgba(47, 93, 58, 0.10) !important; }
.ring-leaf\\/15 { --tw-ring-color: rgba(47, 93, 58, 0.15) !important; }
.ring-emerald-500\\/15 { --tw-ring-color: rgba(16, 185, 129, 0.15) !important; }
.ring-sky-500\\/20 { --tw-ring-color: rgba(14, 165, 233, 0.20) !important; }
.ring-ochre\\/20 { --tw-ring-color: rgba(200, 137, 60, 0.20) !important; }

.h-8\\.5 { height: 2.125rem !important; }
.w-28 { width: 7rem !important; }
.h-28 { height: 7rem !important; }
.w-36 { width: 9rem !important; }
.h-36 { height: 9rem !important; }
.-right-8 { right: -2rem !important; }
.-top-8 { top: -2rem !important; }
.-right-12 { right: -3rem !important; }
.-top-12 { top: -3rem !important; }
.blur-2xl { filter: blur(40px) !important; }
.mb-3\\.5 { margin-bottom: 0.875rem !important; }
.my-2\\.5 { margin-top: 0.625rem !important; margin-bottom: 0.625rem !important; }

.group:hover .group-hover\\/link\\:translate-x-0\\.5 {
  transform: translateX(0.125rem) !important;
}
.group:hover .group-hover\\/btn\\:translate-x-0\\.5 {
  transform: translateX(0.125rem) !important;
}
"""

css_path = 'deploy/hf_space/static/_next/static/chunks/0vn0qenfr622s.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

if '/* === KrishokTech Task-First Decision Hub Refined Styles === */' not in css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write('\n' + css_additions + '\n')
    print("Appended Task-First styles to 0vn0qenfr622s.css")
else:
    print("Styles already present in 0vn0qenfr622s.css")
