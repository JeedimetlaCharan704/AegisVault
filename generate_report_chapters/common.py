import os, base64
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = r'c:\3rd year charan\Hackathon project analysis\aegis-vault'
IMG_DIR = os.path.join(BASE_DIR, 'report_images')

BLACK = RGBColor(0, 0, 0)

def add_p(doc, text="", font_name="Times New Roman", size_pt=12, bold=False, italic=False,
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_sp=1.5, sp_before=0, sp_after=5):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text)
        r.font.name = font_name
        r.font.size = Pt(size_pt)
        r.bold = bold
        r.italic = italic
        r.font.color.rgb = BLACK
    p.alignment = align
    p.paragraph_format.line_spacing = line_sp
    p.paragraph_format.space_before = Pt(sp_before)
    p.paragraph_format.space_after = Pt(sp_after)
    return p

def add_h1(doc, text, align=WD_ALIGN_PARAGRAPH.CENTER, sp_before=14, sp_after=8):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Cambria"
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = BLACK
    p.alignment = align
    p.paragraph_format.space_before = Pt(sp_before)
    p.paragraph_format.space_after = Pt(sp_after)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    return p

def add_h2(doc, text, align=WD_ALIGN_PARAGRAPH.LEFT, sp_before=11, sp_after=4):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = BLACK
    p.alignment = align
    p.paragraph_format.space_before = Pt(sp_before)
    p.paragraph_format.space_after = Pt(sp_after)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    return p

def add_h3(doc, text, align=WD_ALIGN_PARAGRAPH.LEFT, sp_before=8, sp_after=3):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.italic = True
    r.font.color.rgb = BLACK
    p.alignment = align
    p.paragraph_format.space_before = Pt(sp_before)
    p.paragraph_format.space_after = Pt(sp_after)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    return p

def add_img(doc, img_name, width=Inches(4.8), caption=None):
    p_path = os.path.join(IMG_DIR, img_name)
    if os.path.exists(p_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        r = p_img.add_run()
        r.add_picture(p_path, width=width)
        
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            p_cap.paragraph_format.keep_with_next = False
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(11)
            r_cap.italic = True
            r_cap.bold = True
            r_cap.font.color.rgb = BLACK

def apply_ref_table_style(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tblBorders>'
    )
    table._tbl.tblPr.append(tblBorders)

    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for j, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if col_widths and j < len(col_widths):
                cell.width = col_widths[j]
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10.5)
                    r.font.color.rgb = BLACK
                    if i == 0:
                        r.bold = True

def get_base64_img(img_name):
    p_path = os.path.join(IMG_DIR, img_name)
    if os.path.exists(p_path):
        ext = os.path.splitext(img_name)[1].lower().replace('.', '')
        if ext == 'jpg': ext = 'jpeg'
        with open(p_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/{ext};base64,{b64}"
    return ""
