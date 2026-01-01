from rest_framework.views import APIView
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Resume
from .serializers import ResumeSerializer

class CreateResume(APIView):
    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save()
            return Response({"id": resume.id})
        return Response(serializer.errors, status=400)

class ResumeList(APIView):
    def get(self, request):
        resumes = Resume.objects.all()
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

class ResumeDetail(APIView):
    def get(self, request, pk):
        try:
            resume = Resume.objects.get(id=pk)
            serializer = ResumeSerializer(resume)
            return Response(serializer.data)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=404)

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

class DownloadResume(APIView):
    def get(self, request, pk):
        try:
            resume = Resume.objects.get(id=pk)
        except Resume.DoesNotExist:
             return Response({"error": "Resume not found"}, status=404)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

        # Margins: 0.5 inch = 36 points. clean layout.
        doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        Story = []
        styles = getSampleStyleSheet()
        
        # Custom Styles
        styles.add(ParagraphStyle(name='HeaderName', parent=styles['Normal'], alignment=TA_CENTER, fontSize=24, spaceAfter=12, fontName='Helvetica-Bold'))
        styles.add(ParagraphStyle(name='HeaderInfo', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10, spaceAfter=20, fontName='Helvetica'))
        
        styles.add(ParagraphStyle(name='SectionTitle', parent=styles['Normal'], fontSize=12, spaceBefore=12, spaceAfter=6, fontName='Helvetica-Bold', textTransform='uppercase'))
        
        # Content Styles
        styles.add(ParagraphStyle(name='EntryTitle', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold'))
        styles.add(ParagraphStyle(name='EntrySub', parent=styles['Normal'], fontSize=11, fontName='Helvetica'))
        styles.add(ParagraphStyle(name='EntryDate', parent=styles['Normal'], fontSize=11, alignment=TA_RIGHT, fontName='Helvetica'))
        
        bullet_style = ParagraphStyle(name='Bullet', parent=styles['Normal'], fontSize=10, leading=14, fontName='Helvetica')

        def add_divider():
            Story.append(Paragraph("________________________________________________________________________________", styles['Normal']))
            Story.append(Spacer(1, 10))

        # --- HEADER ---
        Story.append(Paragraph(resume.full_name, styles['HeaderName']))
        
        # Info Line
        infos = []
        if resume.location: infos.append(resume.location)
        if resume.phone: infos.append(resume.phone)
        if resume.email: infos.append(resume.email)
        if resume.linkedin_url: infos.append(f'<a href="{resume.linkedin_url}">LinkedIn</a>')
        if resume.github_url: infos.append(f'<a href="{resume.github_url}">GitHub</a>')
        
        Story.append(Paragraph(" | ".join(infos), styles['HeaderInfo']))
        
        # --- SECTIONS HELPER ---
        def create_entry_header(left_bold, left_normal, right_text):
            # Table for aligned header: "Job Title (bold) - Company" ... "Date (right)"
            # We construct the left part as a single paragraph to allow mixed bold/normal
            left_content = f"<b>{left_bold}</b>"
            if left_normal:
                left_content += f" | {left_normal}"
            
            # Using a table for the split alignment
            data = [[Paragraph(left_content, styles['Normal']), Paragraph(right_text, styles['EntryDate'])]]
            t = Table(data, colWidths=[350, 180])
            t.setStyle(TableStyle([
                ('ALIGN', (0,0), (0,0), 'LEFT'),
                ('ALIGN', (1,0), (1,0), 'RIGHT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            return t

        def add_bullets(items):
            if not items: return
            if isinstance(items, str):
                # Fallback if somehow we get a string instead of list
                items = items.split('\n')
            
            bullets = []
            for item in items:
                if item.strip():
                    bullets.append(ListItem(Paragraph(item, bullet_style)))
            
            if bullets:
                Story.append(ListFlowable(bullets, bulletType='bullet', start='circle', leftIndent=10))

        # 1. EDUCATION
        if resume.education:
            Story.append(Paragraph("EDUCATION", styles['SectionTitle']))
            add_divider()
            for edu in resume.education:
                # edu is dict: institution, degree, date, location, grade
                inst = edu.get('institution', '')
                deg = edu.get('degree', '')
                date = edu.get('date', '')
                loc = edu.get('location', '')
                
                # Format: Institution (bold)
                # Degree -- Date (right)
                # This doesn't match strict rules "Institution Name (bold) - Degree ... Date Range aligned to the right"
                # Rule: "Institution Name (bold) ... Degree – Field of Study ... Date Range aligned to the right"
                
                header = create_entry_header(inst, f"{deg} -- {loc}" if loc else deg, date)
                Story.append(header)
                if edu.get('grade'):
                     Story.append(Paragraph(f"Grade: {edu.get('grade')}", styles['EntrySub']))
                Story.append(Spacer(1, 6))

        # 2. EXPERIENCE
        if resume.experience:
            Story.append(Paragraph("EXPERIENCE", styles['SectionTitle']))
            add_divider()
            for exp in resume.experience:
                # exp: title, company, date, location, description (list)
                title = exp.get('title', '')
                comp = exp.get('company', '')
                date = exp.get('date', '')
                loc = exp.get('location', '')
                desc = exp.get('description', [])
                
                # Rule: Job Title (bold) - Company Name ... Date Range (Right)
                header = create_entry_header(title, f"{comp} ({loc})", date)
                Story.append(header)
                add_bullets(desc)
                Story.append(Spacer(1, 8))

        # 3. PROJECTS
        if resume.projects:
            Story.append(Paragraph("PROJECTS", styles['SectionTitle']))
            add_divider()
            for proj in resume.projects:
                # proj: title, tech, description (list), link
                title = proj.get('title', '')
                tech = proj.get('tech', '')
                desc = proj.get('description', [])
                link = proj.get('link', '')
                
                # Rule: Project Title (bold) ... Tech used (italic/parens)
                left_text = title
                if tech:
                    left_text += f" <i>({tech})</i>"
                
                Story.append(Paragraph(f"<b>{title}</b>" + (f" | <i>{tech}</i>" if tech else ""), styles['EntrySub']))
                add_bullets(desc)
                if link:
                    Story.append(Paragraph(f"<a href='{link}'>{link}</a>", styles['Bullet']))
                Story.append(Spacer(1, 8))

        # 4. TECHNICAL SKILLS
        if resume.skills:
             Story.append(Paragraph("TECHNICAL SKILLS", styles['SectionTitle']))
             add_divider()
             # skills: dict or list of dicts {category: "...", items: "..."}
             if isinstance(resume.skills, dict):
                 for cat, items in resume.skills.items():
                     Story.append(Paragraph(f"<b>{cat}:</b> {items}", styles['Normal']))
             elif isinstance(resume.skills, list):
                 for skill_group in resume.skills:
                     cat = skill_group.get('category', '')
                     val = skill_group.get('items', '')
                     Story.append(Paragraph(f"<b>{cat}:</b> {val}", styles['Normal']))
             Story.append(Spacer(1, 6))

        # 5. CERTIFICATIONS
        if resume.certifications:
            Story.append(Paragraph("CERTIFICATIONS", styles['SectionTitle']))
            add_divider()
            # certs: list of strings or objects
            # Rule: Bullet list, Cert Name - Issuing Org
            bullets = []
            for cert in resume.certifications:
                if isinstance(cert, str):
                    bullets.append(cert)
                elif isinstance(cert, dict):
                    name = cert.get('name', '')
                    org = cert.get('organization', '')
                    bullets.append(f"{name} - {org}")
            
            add_bullets(bullets)

        doc.build(Story)
        return response
