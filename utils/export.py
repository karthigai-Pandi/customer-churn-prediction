"""
Utility Functions: Export Functionality
Handles exporting prediction data to PDF and CSV
"""
import csv
from io import StringIO, BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExportManager:
    """
    Handles export of prediction data to different formats
    """
    
    @staticmethod
    def export_to_csv(predictions, filename=None):
        """
        Export predictions to CSV format
        
        Args:
            predictions: List of prediction dictionaries
            filename: Output filename (optional)
            
        Returns:
            CSV content as string or saves to file
        """
        try:
            if not predictions:
                logger.warning("No predictions to export")
                return None
            
            output = StringIO()
            fieldnames = predictions[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(predictions)
            
            csv_content = output.getvalue()
            
            if filename:
                with open(filename, 'w', newline='') as f:
                    f.write(csv_content)
                logger.info(f"CSV exported to {filename}")
            
            return csv_content
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            raise
    
    @staticmethod
    def export_to_pdf(predictions, title="Churn Prediction Report", filename=None):
        """
        Export predictions to PDF format
        
        Args:
            predictions: List of prediction dictionaries
            title: Report title
            filename: Output filename (optional)
            
        Returns:
            PDF content as bytes or saves to file
        """
        try:
            if not predictions:
                logger.warning("No predictions to export")
                return None
            
            # Create PDF document
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#003366'),
                spaceAfter=30,
                alignment=1
            )
            elements.append(Paragraph(title, title_style))
            
            # Report info
            report_info_style = ParagraphStyle(
                'ReportInfo',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.grey
            )
            elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                    report_info_style))
            elements.append(Paragraph(f"Total Records: {len(predictions)}", report_info_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # Create table data
            table_data = [list(predictions[0].keys())]  # Header
            for pred in predictions:
                table_data.append(list(pred.values()))
            
            # Create table
            table = Table(table_data, colWidths=[1.2*inch]*len(predictions[0].keys()))
            
            # Style table
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ])
            
            table.setStyle(table_style)
            elements.append(table)
            
            # Build PDF
            doc.build(elements)
            pdf_content = buffer.getvalue()
            buffer.close()
            
            if filename:
                with open(filename, 'wb') as f:
                    f.write(pdf_content)
                logger.info(f"PDF exported to {filename}")
            
            return pdf_content
        except Exception as e:
            logger.error(f"Error exporting to PDF: {str(e)}")
            raise
    
    @staticmethod
    def export_statistics(stats_dict, format='csv'):
        """
        Export statistics to specified format
        
        Args:
            stats_dict: Dictionary with statistics
            format: 'csv' or 'pdf'
            
        Returns:
            Exported content
        """
        try:
            predictions = [stats_dict]
            
            if format.lower() == 'csv':
                return ExportManager.export_to_csv(predictions)
            elif format.lower() == 'pdf':
                return ExportManager.export_to_pdf(predictions, title="Model Statistics Report")
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            logger.error(f"Error exporting statistics: {str(e)}")
            raise
