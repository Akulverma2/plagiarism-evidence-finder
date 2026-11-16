"""Document visualizer and HTML highlighter for Plagiarism Evidence Finder.

Generates SaaS-grade side-by-side document comparison markup:
- Professional typography (Inter/system-ui)
- Sophisticated subtle pastel highlight palettes (Linear/Notion inspired)
- Interactive hover tooltips and minimal pill badges
- Strict preservation of original document casing, spacing, and formatting
"""

import html
from typing import List, Tuple
from src.algorithms.common import Token, MatchInterval


# Linear / Notion inspired subtle pastel highlight palette
HIGHLIGHT_COLORS = [
    {"bg": "#EEF2FF", "border": "#C7D2FE", "text": "#3730A3", "badge": "#6366F1"},  # Indigo
    {"bg": "#ECFDF5", "border": "#A7F3D0", "text": "#065F46", "badge": "#10B981"},  # Emerald
    {"bg": "#FFFBEB", "border": "#FDE68A", "text": "#92400E", "badge": "#F59E0B"},  # Amber
    {"bg": "#F5F3FF", "border": "#DDD6FE", "text": "#5B21B6", "badge": "#8B5CF6"},  # Violet
    {"bg": "#F0F9FF", "border": "#BAE6FD", "text": "#075985", "badge": "#0EA5E9"},  # Sky
    {"bg": "#FFF1F2", "border": "#FECDD3", "text": "#9F1239", "badge": "#F43F5E"},  # Rose
]


def generate_highlighted_html(
    original_text: str,
    tokens: List[Token],
    intervals: List[MatchInterval],
    is_suspect: bool = True
) -> str:
    """Generate styled HTML markup of the text with highlighted match intervals.
    
    Args:
        original_text: Full raw un-normalized text string.
        tokens: Tokenized words with exact character offset mapping.
        intervals: Merged MatchIntervals.
        is_suspect: True if rendering suspect document, False for source.
        
    Returns:
        Safe HTML string ready to render in Streamlit.
    """
    if not original_text:
        return (
            "<div style='display: flex; align-items: center; justify-content: center; height: 280px; "
            "color: #94A3B8; font-family: Inter, sans-serif; font-size: 14px;'>"
            "No document content to display. Upload or paste a document to begin analysis.</div>"
        )

    if not intervals or not tokens:
        escaped_text = html.escape(original_text)
        return (
            f"<div style='font-family: \"JetBrains Mono\", \"Fira Code\", Consolas, monospace; "
            f"white-space: pre-wrap; line-height: 1.7; font-size: 13.5px; color: #334155; padding: 18px; "
            f"background: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0;'>{escaped_text}</div>"
        )

    # Build character-level spans to highlight
    char_spans: List[Tuple[int, int, int, MatchInterval]] = []

    for p_idx, interval in enumerate(intervals):
        if is_suspect:
            s_tok = interval.suspect_start
            e_tok = interval.suspect_end
        else:
            s_tok = interval.source_start
            e_tok = interval.source_end

        if s_tok < len(tokens) and e_tok < len(tokens):
            c_start = tokens[s_tok].char_start
            c_end = tokens[e_tok].char_end
            char_spans.append((c_start, c_end, p_idx, interval))

    # Sort spans by start character
    char_spans.sort(key=lambda x: x[0])

    html_parts = []
    last_idx = 0

    for c_start, c_end, p_idx, interval in char_spans:
        # Non-highlighted prefix text
        if c_start > last_idx:
            html_parts.append(html.escape(original_text[last_idx:c_start]))

        # Highlighted text
        span_text = original_text[c_start:c_end]
        palette = HIGHLIGHT_COLORS[p_idx % len(HIGHLIGHT_COLORS)]

        if is_suspect:
            tooltip = f"Passage #{p_idx + 1} • {interval.length} words • Suspect [{interval.suspect_start}..{interval.suspect_end}] → Source [{interval.source_start}..{interval.source_end}]"
        else:
            tooltip = f"Passage #{p_idx + 1} • {interval.length} words • Source [{interval.source_start}..{interval.source_end}]"

        highlight_markup = (
            f'<mark title="{html.escape(tooltip)}" style="'
            f'background-color: {palette["bg"]}; '
            f'border: 1px solid {palette["border"]}; '
            f'color: {palette["text"]}; '
            f'padding: 1px 4px; '
            f'border-radius: 4px; '
            f'font-weight: 500; '
            f'transition: all 0.15s ease-in-out; '
            f'display: inline; '
            f'box-decoration-break: clone; '
            f'-webkit-box-decoration-break: clone;">'
            f'<span style="font-size: 10px; font-weight: 700; background: {palette["badge"]}; '
            f'color: #FFFFFF; border-radius: 3px; padding: 1px 4px; margin-right: 4px; vertical-align: middle; '
            f'letter-spacing: 0.3px;">#{p_idx + 1}</span>'
            f'{html.escape(span_text)}'
            f'</mark>'
        )
        html_parts.append(highlight_markup)
        last_idx = max(last_idx, c_end)

    # Remaining suffix
    if last_idx < len(original_text):
        html_parts.append(html.escape(original_text[last_idx:]))

    container_html = (
        f'<div style="'
        f'background-color: #FFFFFF; '
        f'color: #1E293B; '
        f'border: 1px solid #E2E8F0; '
        f'border-radius: 8px; '
        f'padding: 18px 20px; '
        f'font-family: -apple-system, BlinkMacSystemFont, \'Inter\', \'Segoe UI\', Roboto, sans-serif; '
        f'font-size: 13.5px; '
        f'line-height: 1.75; '
        f'white-space: pre-wrap; '
        f'word-break: break-word; '
        f'max-height: 520px; '
        f'overflow-y: auto; '
        f'box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);">'
        f'{"".join(html_parts)}'
        f'</div>'
    )
    return container_html
