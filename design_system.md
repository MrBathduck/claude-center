# Design System

> This file defines the design tokens, components, and patterns for this project.
> The UI/UX Designer agent uses this file to ensure consistency.
>
> **Instructions:** Fill in the sections below with your project's actual values.
> Delete any sections that don't apply to your project.

---

## Colors

### Brand Colors
| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary` | `#3B82F6` | Primary actions, links, focus states |
| `--color-secondary` | `#6B7280` | Secondary actions, less emphasis |
| `--color-accent` | `#8B5CF6` | Highlights, special elements |

### Semantic Colors
| Token | Value | Usage |
|-------|-------|-------|
| `--color-success` | `#10B981` | Success states, confirmations |
| `--color-warning` | `#F59E0B` | Warnings, caution states |
| `--color-error` | `#EF4444` | Errors, destructive actions |
| `--color-info` | `#3B82F6` | Informational messages |

### Neutral Colors
| Token | Value | Usage |
|-------|-------|-------|
| `--color-background` | `#FFFFFF` | Page background |
| `--color-surface` | `#F9FAFB` | Card backgrounds, elevated surfaces |
| `--color-border` | `#E5E7EB` | Borders, dividers |
| `--color-text-primary` | `#111827` | Primary text |
| `--color-text-secondary` | `#6B7280` | Secondary text, labels |
| `--color-text-muted` | `#9CA3AF` | Placeholder text, disabled |

---

## Typography

### Font Families
| Token | Value | Usage |
|-------|-------|-------|
| `--font-sans` | `'Inter', system-ui, sans-serif` | Body text, UI elements |
| `--font-mono` | `'Fira Code', monospace` | Code blocks, technical content |

### Font Sizes
| Token | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `--text-xs` | `0.75rem` | `1rem` | Captions, badges |
| `--text-sm` | `0.875rem` | `1.25rem` | Secondary text, labels |
| `--text-base` | `1rem` | `1.5rem` | Body text |
| `--text-lg` | `1.125rem` | `1.75rem` | Large body text |
| `--text-xl` | `1.25rem` | `1.75rem` | Section headings |
| `--text-2xl` | `1.5rem` | `2rem` | Page headings |
| `--text-3xl` | `1.875rem` | `2.25rem` | Large headings |

### Font Weights
| Token | Value | Usage |
|-------|-------|-------|
| `--font-normal` | `400` | Body text |
| `--font-medium` | `500` | Emphasis, labels |
| `--font-semibold` | `600` | Subheadings, buttons |
| `--font-bold` | `700` | Headings, strong emphasis |

---

## Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--space-0` | `0` | No spacing |
| `--space-1` | `0.25rem` | Tight spacing (4px) |
| `--space-2` | `0.5rem` | Small spacing (8px) |
| `--space-3` | `0.75rem` | Compact spacing (12px) |
| `--space-4` | `1rem` | Default spacing (16px) |
| `--space-5` | `1.25rem` | Medium spacing (20px) |
| `--space-6` | `1.5rem` | Comfortable spacing (24px) |
| `--space-8` | `2rem` | Large spacing (32px) |
| `--space-10` | `2.5rem` | Extra large spacing (40px) |
| `--space-12` | `3rem` | Section spacing (48px) |

---

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-none` | `0` | Sharp corners |
| `--radius-sm` | `0.125rem` | Subtle rounding |
| `--radius-md` | `0.375rem` | Default rounding |
| `--radius-lg` | `0.5rem` | Card rounding |
| `--radius-xl` | `0.75rem` | Modal rounding |
| `--radius-full` | `9999px` | Pill shapes, avatars |

---

## Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle elevation |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.1)` | Cards, dropdowns |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |
| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.15)` | Elevated dialogs |

---

## Breakpoints

| Token | Value | Description |
|-------|-------|-------------|
| `--bp-sm` | `640px` | Small devices (landscape phones) |
| `--bp-md` | `768px` | Medium devices (tablets) |
| `--bp-lg` | `1024px` | Large devices (desktops) |
| `--bp-xl` | `1280px` | Extra large devices |
| `--bp-2xl` | `1536px` | Very large screens |

---

## Animation

### Durations
| Token | Value | Usage |
|-------|-------|-------|
| `--duration-fast` | `100ms` | Micro-interactions (hover, focus) |
| `--duration-normal` | `200ms` | Standard transitions |
| `--duration-slow` | `300ms` | Larger animations |
| `--duration-slower` | `500ms` | Page transitions, complex animations |

### Easing
| Token | Value | Usage |
|-------|-------|-------|
| `--ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Elements exiting |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Elements entering |
| `--ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Elements moving |

---

## Components

### Buttons
| Variant | Class/Token | Usage |
|---------|-------------|-------|
| Primary | `.btn-primary` | Main actions (Submit, Save, Confirm) |
| Secondary | `.btn-secondary` | Secondary actions (Cancel, Back) |
| Outline | `.btn-outline` | Tertiary actions, less emphasis |
| Ghost | `.btn-ghost` | Minimal actions, icon buttons |
| Danger | `.btn-danger` | Destructive actions (Delete, Remove) |

### Form Elements
| Component | Location | Notes |
|-----------|----------|-------|
| Input | `src/components/Input.tsx` | Text, email, password fields |
| Select | `src/components/Select.tsx` | Dropdown selections |
| Checkbox | `src/components/Checkbox.tsx` | Boolean selections |
| Radio | `src/components/Radio.tsx` | Single selection from group |
| Textarea | `src/components/Textarea.tsx` | Multi-line text input |

### Feedback Components
| Component | Location | Usage |
|-----------|----------|-------|
| Toast | `src/components/Toast.tsx` | Temporary notifications |
| Alert | `src/components/Alert.tsx` | Inline messages |
| Modal | `src/components/Modal.tsx` | Dialogs, confirmations |
| Skeleton | `src/components/Skeleton.tsx` | Loading placeholders |

---

## Patterns

### Loading States
- **Initial load:** Use `<Skeleton />` components matching content shape
- **Action pending:** Use spinner inside button, disable button
- **Background refresh:** Show subtle indicator, don't block UI

### Error States
- **Form errors:** Inline red text below field, red border
- **Page errors:** Full error component with retry action
- **Toast errors:** For non-blocking errors, auto-dismiss after 5s

### Empty States
- **Lists:** Illustration + message + primary action
- **Search:** "No results" + suggestions
- **Filters:** "No matches" + clear filters button

### Confirmation Patterns
- **Destructive actions:** Require explicit confirmation modal
- **Reversible actions:** Use toast with undo option
- **Auto-save:** Show "Saved" indicator, no confirmation needed

---

## Accessibility

### Focus States
- All interactive elements MUST have visible focus indicator
- Focus ring: `2px solid var(--color-primary)` with `2px offset`

### Color Contrast
- Normal text: minimum 4.5:1 ratio
- Large text (18px+): minimum 3:1 ratio
- UI components: minimum 3:1 ratio

### Keyboard Navigation
- Tab order follows visual order
- All actions reachable via keyboard
- Escape closes modals/dropdowns
- Enter activates focused element

---

## File Locations

| Asset Type | Location |
|------------|----------|
| Global styles | `src/styles/globals.css` |
| CSS variables | `src/styles/variables.css` |
| Component styles | `src/components/[Component]/styles.css` |
| Tailwind config | `tailwind.config.js` |
| Theme tokens | `src/styles/theme.ts` |
