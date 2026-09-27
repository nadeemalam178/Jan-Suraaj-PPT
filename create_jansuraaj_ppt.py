import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
import os

# ── Customizations & Colors ─────────────────────────────────────
PRIMARY_COLOR = RGBColor(0x11, 0x24, 0x54)    # Dark Navy Blue
SECONDARY_COLOR = RGBColor(0x28, 0x52, 0x8C)  # Lighter Blue
ACCENT_COLOR = RGBColor(0xDB, 0xA2, 0x3A)     # Gold / Mustard
BG_COLOR = RGBColor(0xF5, 0xF7, 0xFA)         # Light Gray/Blue Bg
TEXT_LIGHT = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_DARK = RGBColor(0x1F, 0x29, 0x37)
BODY_TEXT = RGBColor(0x33, 0x33, 0x33)

# ── Image paths ────────────────────────────────────────────────
IMG_DIR = r"c:\Users\alamn\Downloads\JS PPT\real_images"
IMAGES = {
    "title": os.path.join(IMG_DIR, "title.jpg"),
    "padyatra": os.path.join(IMG_DIR, "padyatra.jpg"),
    "party_launch": os.path.join(IMG_DIR, "party_launch.jpg"),
    "victory": os.path.join(IMG_DIR, "victory.jpg"),
    "ashram": os.path.join(IMG_DIR, "ashram.jpg"),
    "campaign": os.path.join(IMG_DIR, "campaign.jpg"),
    "bpsc_protest": os.path.join(IMG_DIR, "bpsc_protest.jpg"),
    "timeline": os.path.join(IMG_DIR, "timeline.png"),
}

# ── Presentation Setup ─────────────────────────────────────────
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SLIDE_W, SLIDE_H = Inches(13.333), Inches(7.5)

blank_slide_layout = prs.slide_layouts[6] 

def add_shape_bg(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_textbox(slide, text, left, top, width, height, font_size=Pt(18), font_color=BODY_TEXT, bold=False, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tb.text_frame.word_wrap = True
    p = tb.text_frame.paragraphs[0]
    p.text = text
    p.font.size = font_size
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.name = "Inter"
    p.alignment = align
    return tb

def add_title(slide, text, subtitle=None):
    add_shape_bg(slide, 0, 0, SLIDE_W, Inches(1.2), PRIMARY_COLOR)
    add_textbox(slide, text, Inches(0.5), Inches(0.2), Inches(12), Inches(0.6), font_size=Pt(36), font_color=TEXT_LIGHT, bold=True)
    if subtitle:
        add_textbox(slide, subtitle, Inches(0.5), Inches(0.8), Inches(12), Inches(0.4), font_size=Pt(18), font_color=ACCENT_COLOR, bold=False)
    add_shape_bg(slide, 0, Inches(1.2), SLIDE_W, Inches(0.05), ACCENT_COLOR)

def add_image_safe(slide, img_key, left, top, width, height):
    path = IMAGES.get(img_key)
    if path and os.path.exists(path):
        try:
            return slide.shapes.add_picture(path, left, top, width, height)
        except Exception as e:
            pass
    # Fallback
    s = add_shape_bg(slide, left, top, width, height, RGBColor(0xDD, 0xDD, 0xDD))
    add_textbox(slide, "[Image Missing]", left, top, width, height, align=PP_ALIGN.CENTER)
    return s

def add_data_table(slide, left, top, width, height, data, col_widths):
    rows = len(data)
    cols = len(data[0])
    shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = shape.table
    
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(14)
                p.font.name = "Inter"
                if r_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = TEXT_LIGHT
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = PRIMARY_COLOR
                else:
                    p.font.color.rgb = BODY_TEXT

# ── Slides Generation ──────────────────────────────────────────

# Slide 1: Title Slide
slide1 = prs.slides.add_slide(blank_slide_layout)
add_image_safe(slide1, "title", 0, 0, SLIDE_W, SLIDE_H)
add_shape_bg(slide1, 0, 0, SLIDE_W, SLIDE_H, RGBColor(0, 0, 0)) # Dim overlay
slide1.shapes[-1].fill.transparency = 0.5 
add_textbox(slide1, "Jan Suraaj: The Complete Journey", Inches(1), Inches(2.5), Inches(11.3), Inches(1.5), font_size=Pt(64), font_color=TEXT_LIGHT, bold=True, align=PP_ALIGN.CENTER)
add_textbox(slide1, "2022 to 2026: From Padyatra to Political Victory", Inches(1), Inches(3.8), Inches(11.3), Inches(0.8), font_size=Pt(28), font_color=ACCENT_COLOR, bold=True, align=PP_ALIGN.CENTER)
add_textbox(slide1, "A movement for Bihar's transformation", Inches(1), Inches(4.5), Inches(11.3), Inches(0.5), font_size=Pt(20), font_color=TEXT_LIGHT, bold=False, align=PP_ALIGN.CENTER)

# Slide 2: Prashant Kishor & The Vision
slide2 = prs.slides.add_slide(blank_slide_layout)
add_title(slide2, "The Visionary: Prashant Kishor", "Background & Inspiration")
add_textbox(slide2, "• Former UN public health official turned political strategist.\n• Managed highly successful campaigns across India before turning focus to his home state, Bihar.\n• Inspired by Jayaprakash Narayan (Sitab Diara) and Mahatma Gandhi.\n• The 1280 Days Documentary highlights his realization during Covid-19 lockdowns about the plight of Bihari migrants (Palayan), extreme poverty (Garibi), and unemployment (Rojgar).", Inches(0.5), Inches(1.5), Inches(12), Inches(3), font_size=Pt(20))
add_image_safe(slide2, "party_launch", Inches(0.5), Inches(4.5), Inches(12.3), Inches(2.5))

# Slide 3: 2022 - Genesis & Padyatra
slide3 = prs.slides.add_slide(blank_slide_layout)
add_title(slide3, "2022: The Genesis of Jan Suraaj", "Oct 2: Launch of the Historic Padyatra")
add_image_safe(slide3, "ashram", Inches(0.5), Inches(1.5), Inches(6), Inches(5.5))
add_textbox(slide3, "Bhitiharwa Gandhi Ashram", Inches(7), Inches(1.5), Inches(5.8), Inches(0.5), font_size=Pt(24), font_color=PRIMARY_COLOR, bold=True)
add_textbox(slide3, "• Launched exactly where Mahatma Gandhi started his Satyagraha.\n• The 3,500 km Padyatra (foot march) was designed to cover all 38 districts of Bihar.\n• Goal: Understand grassroots problems without relying on intermediaries.\n• Over 1280 days of intense struggle connecting directly with villages.", Inches(7), Inches(2.2), Inches(5.8), Inches(4), font_size=Pt(18))

# Slide 4: 2023 - Building the Groundwork
slide4 = prs.slides.add_slide(blank_slide_layout)
add_title(slide4, "2023: Grassroots Expansion", "Connecting with every Panchayat")
add_textbox(slide4, "Organizational Building", Inches(0.5), Inches(1.5), Inches(5.8), Inches(0.5), font_size=Pt(24), font_color=PRIMARY_COLOR, bold=True)
add_textbox(slide4, "• Padyatra continues, gathering massive support across Bihar.\n• April 2023: Jan Suraaj registers its first political win with Afaq Ahmad securing the Saran Teachers Constituency in the Bihar Legislative Council.\n• The movement focuses heavily on youth empowerment and the Jan Suraaj Fellowship program.", Inches(0.5), Inches(2.2), Inches(5.8), Inches(4), font_size=Pt(18))
add_image_safe(slide4, "padyatra", Inches(6.8), Inches(1.5), Inches(6), Inches(5.5))

# Slide 5: 2024 - Party Launch & Elections
slide5 = prs.slides.add_slide(blank_slide_layout)
add_title(slide5, "2024: The Jan Suraaj Party", "From Movement to Political Platform")
add_textbox(slide5, "• Oct 2, 2024: Official launch of the Jan Suraaj Party in Patna.\n• Symbol: The 'School Bag', emphasizing Education as the path to liberation.\n• Nov 2024: Contested by-elections in Tarari, Ramgarh, Belaganj, and Imamganj. Secured nearly 10% vote share despite not winning seats, establishing a strong foundation.", Inches(0.5), Inches(1.5), Inches(12), Inches(2), font_size=Pt(20))
add_image_safe(slide5, "campaign", Inches(0.5), Inches(3.5), Inches(12.3), Inches(3.5))

# Slide 6: Jan 2025 - The BPSC Protest
slide6 = prs.slides.add_slide(blank_slide_layout)
add_title(slide6, "January 2025: Fighting for the Youth", "BPSC Hunger Strike")
add_image_safe(slide6, "bpsc_protest", Inches(0.5), Inches(1.5), Inches(6), Inches(5.5))
add_textbox(slide6, "The Gandhi Maidan Hunger Strike", Inches(7), Inches(1.5), Inches(5.8), Inches(0.5), font_size=Pt(24), font_color=PRIMARY_COLOR, bold=True)
add_textbox(slide6, "• Prashant Kishor undertook a 14-day hunger strike (Aamran Anshan) demanding justice for students regarding BPSC paper leaks.\n• Met with severe police action and FIRs, but stood firm.\n• Established Jan Suraaj as the primary voice of the youth against systemic corruption.", Inches(7), Inches(2.2), Inches(5.8), Inches(4), font_size=Pt(18))

# Slide 7: 2025 Assembly Elections & Restructuring
slide7 = prs.slides.add_slide(blank_slide_layout)
add_title(slide7, "2025: The Assembly Elections", "Challenges and Restructuring")
add_textbox(slide7, "Electoral Challenge", Inches(0.5), Inches(1.5), Inches(12), Inches(0.5), font_size=Pt(24), font_color=PRIMARY_COLOR, bold=True)
add_textbox(slide7, "• Contested 238 out of 243 seats in the Bihar Assembly Elections.\n• Faced immense polarization and resource challenges against established alliances (NDA/Mahagathbandhan).\n• Despite immense effort, the party did not win seats and secured ~3.4% vote share.\n• Nov 2025: Prashant Kishor announces complete dissolution of the party structure to rebuild from scratch.", Inches(0.5), Inches(2.1), Inches(12), Inches(2.5), font_size=Pt(18))

# Slide 8: 2026 - The Historic Bankipur Victory
slide8 = prs.slides.add_slide(blank_slide_layout)
add_title(slide8, "2026: The Breakthrough", "Bankipur By-Election Victory")
add_image_safe(slide8, "victory", Inches(0.5), Inches(1.5), Inches(6), Inches(5.5))
add_textbox(slide8, "Prashant Kishor's Electoral Win", Inches(7), Inches(1.5), Inches(5.8), Inches(0.5), font_size=Pt(24), font_color=PRIMARY_COLOR, bold=True)
add_textbox(slide8, "• July 30, 2026: Prashant Kishor wins his first election from the Bankipur constituency in Patna.\n• Defeated BJP's Neeraj Kumar by a massive margin.\n• This victory marked the ultimate validation of the 1280+ days of struggle and padyatra.", Inches(7), Inches(2.2), Inches(5.8), Inches(4), font_size=Pt(18))

# Slide 9: 2026 Bankipur Data
slide9 = prs.slides.add_slide(blank_slide_layout)
add_title(slide9, "Bankipur By-Election Results", "Statistical Breakdown")
data = [
    ["Candidate", "Party", "Votes", "Vote Share (%)"],
    ["Prashant Kishor", "Jan Suraaj", "64,151", "49.23%"],
    ["Neeraj Kumar", "BJP", "44,827", "34.40%"],
    ["Luv Sinha", "INC (Mahagathbandhan)", "15,234", "11.69%"],
    ["Others/NOTA", "-", "6,095", "4.68%"]
]
col_widths = [Inches(3), Inches(3), Inches(2.5), Inches(2.5)]
add_data_table(slide9, Inches(1.2), Inches(2.5), Inches(11), Inches(3), data, col_widths)

# Slide 10: Conclusion
slide10 = prs.slides.add_slide(blank_slide_layout)
add_title(slide10, "The Road Ahead", "Transforming Bihar")
add_textbox(slide10, "A New Dawn for Bihar", Inches(0.5), Inches(1.5), Inches(12), Inches(0.5), font_size=Pt(24), font_color=PRIMARY_COLOR, bold=True)
add_textbox(slide10, "• The Bankipur victory is just the beginning.\n• The mission remains: Stopping migration, providing world-class education, and generating employment.\n• Jan Suraaj continues its journey as a mass movement dedicated to systemic change.", Inches(0.5), Inches(2.2), Inches(12), Inches(2), font_size=Pt(20))
add_image_safe(slide10, "timeline", Inches(0.5), Inches(4.5), Inches(12.3), Inches(2.5))

prs.save("Jan Suraaj Complete Journey 2022-2026.pptx")
print("\n✅ Presentation saved successfully!")
print("📁 Location: Jan Suraaj Complete Journey 2022-2026.pptx")
print("📊 Total Slides: 10")
