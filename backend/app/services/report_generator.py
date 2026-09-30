from typing import Dict
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from app.config import settings


class ReportGenerator:
    """Generate PDF plagiarism reports."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            leading=14
        ))
        
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.gray,
            italic=True,
            alignment=TA_CENTER
        ))
    
    def generate_report(
        self,
        comparison_data: Dict,
        user_name: str,
        output_path: str
    ) -> str:
        """Generate a PDF report for a comparison."""
        # Create report directory if it doesn't exist
        report_dir = Path(settings.report_dir)
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Create PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Title
        story.append(Paragraph("Semantic Plagiarism Detection Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        metadata = [
            ['Report ID:', str(comparison_data.get('id', 'N/A'))],
            ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['User:', user_name],
            ['Reference Document:', comparison_data.get('reference_filename', 'N/A')],
            ['Submitted Document:', comparison_data.get('submitted_filename', 'N/A')],
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1e3a8a')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        story.append(metadata_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Overall similarity
        overall_similarity = comparison_data.get('overall_similarity', 0)
        similarity_percentage = overall_similarity * 100
        
        story.append(Paragraph("Overall Similarity", self.styles['CustomHeading']))
        story.append(Paragraph(
            f"<b>{similarity_percentage:.1f}%</b> - {self._get_similarity_label(overall_similarity)}",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.2*inch))
        
        # Statistics
        stats = comparison_data.get('statistics', {})
        story.append(Paragraph("Statistics", self.styles['CustomHeading']))
        
        stats_data = [
            ['Metric', 'Value'],
            ['Weighted Similarity', f"{stats.get('weighted_similarity', 0) * 100:.1f}%"],
            ['Text with Matches', f"{stats.get('percentage_of_text_with_matches', 0):.1f}%"],
            ['Total Chunks', str(stats.get('total_submitted_chunks', 0))],
            ['Matching Chunks', str(stats.get('matching_chunk_count', 0))],
            ['Very High Similarity', str(stats.get('very_high_similarity_chunk_count', 0))],
            ['High Similarity', str(stats.get('high_similarity_chunk_count', 0))],
            ['Moderate Similarity', str(stats.get('moderate_similarity_chunk_count', 0))],
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 2.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Matching sections
        matches = comparison_data.get('matches', [])
        if matches:
            story.append(Paragraph("Matching Sections", self.styles['CustomHeading']))
            
            for i, match in enumerate(matches[:20], 1):  # Limit to top 20 matches
                story.append(Paragraph(f"Match #{i}", self.styles['CustomHeading']))
                
                match_info = [
                    ['Similarity:', f"{match['combined_score'] * 100:.1f}%"],
                    ['Classification:', match['classification']],
                    ['Semantic Score:', f"{match['semantic_score'] * 100:.1f}%"],
                    ['Lexical Score:', f"{match['lexical_score'] * 100:.1f}%"],
                    ['N-gram Score:', f"{match['ngram_score'] * 100:.1f}%"],
                ]
                
                match_table = Table(match_info, colWidths=[1.5*inch, 3.5*inch])
                match_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]))
                
                story.append(match_table)
                story.append(Spacer(1, 0.1*inch))
                
                # Reference text
                story.append(Paragraph("Reference Text:", self.styles['CustomBody']))
                ref_text = match['reference_chunk']['text'][:500]
                if len(match['reference_chunk']['text']) > 500:
                    ref_text += "..."
                story.append(Paragraph(ref_text, self.styles['CustomBody']))
                story.append(Spacer(1, 0.1*inch))
                
                # Submitted text
                story.append(Paragraph("Submitted Text:", self.styles['CustomBody']))
                sub_text = match['submitted_chunk']['text'][:500]
                if len(match['submitted_chunk']['text']) > 500:
                    sub_text += "..."
                story.append(Paragraph(sub_text, self.styles['CustomBody']))
                story.append(Spacer(1, 0.1*inch))
                
                # Explanation
                story.append(Paragraph("Explanation:", self.styles['CustomBody']))
                story.append(Paragraph(match['explanation'], self.styles['CustomBody']))
                story.append(Spacer(1, 0.2*inch))
                
                if i < len(matches[:20]):
                    story.append(Spacer(1, 0.1*inch))
        
        # Disclaimer
        story.append(PageBreak())
        story.append(Paragraph(
            "Disclaimer",
            self.styles['CustomHeading']
        ))
        story.append(Paragraph(
            "This report provides similarity indicators based on computational text analysis. "
            "It is not a definitive determination of academic misconduct. Final interpretation should "
            "be performed by a qualified human reviewer and should consider citations, common terminology, "
            "assignment requirements, and source context.",
            self.styles['Disclaimer']
        ))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _get_similarity_label(self, score: float) -> str:
        """Get label for similarity score."""
        if score >= 0.80:
            return "Very High"
        elif score >= 0.65:
            return "High"
        elif score >= 0.45:
            return "Moderate"
        else:
            return "Low"
