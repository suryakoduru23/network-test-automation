"""Report Generation Service"""
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models import Report, TestRun
from app.schemas.report import ReportGenerateRequest
import logging

logger = logging.getLogger(__name__)


class ReportService:
    """Report Generation Service"""
    
    @staticmethod
    def generate_report(
        db: Session,
        request: ReportGenerateRequest
    ) -> Report:
        """Generate test report"""
        try:
            # Query test runs in date range
            test_runs = db.query(TestRun).filter(
                TestRun.created_at >= request.start_date,
                TestRun.created_at <= request.end_date
            ).all()
            
            # Calculate statistics
            total_tests = len(test_runs)
            passed_tests = len([t for t in test_runs if t.status == "passed"])
            failed_tests = len([t for t in test_runs if t.status == "failed"])
            success_rate = f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"
            
            # Create report
            report = Report(
                title=request.title,
                description=request.description,
                report_format=request.report_format,
                status="completed",
                start_date=request.start_date,
                end_date=request.end_date,
                test_count=total_tests,
                passed_count=passed_tests,
                failed_count=failed_tests,
                success_rate=success_rate,
                generated_at=datetime.utcnow()
            )
            
            db.add(report)
            db.commit()
            db.refresh(report)
            logger.info(f"Report generated: {report.id}")
            return report
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            raise
    
    @staticmethod
    def get_report(db: Session, report_id: int) -> Optional[Report]:
        """Get report by ID"""
        return db.query(Report).filter(Report.id == report_id).first()
    
    @staticmethod
    def get_all_reports(db: Session) -> List[Report]:
        """Get all reports"""
        return db.query(Report).order_by(Report.created_at.desc()).all()
    
    @staticmethod
    def export_report(report: Report, format: str) -> str:
        """Export report in specified format"""
        if format == "html":
            return ReportService._generate_html_report(report)
        elif format == "csv":
            return ReportService._generate_csv_report(report)
        elif format == "pdf":
            return ReportService._generate_pdf_report(report)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    @staticmethod
    def _generate_html_report(report: Report) -> str:
        """Generate HTML report"""
        html = f"""
        <html>
            <head>
                <title>{report.title}</title>
                <style>
                    body {{ font-family: Arial; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                    th {{ background-color: #4CAF50; color: white; }}
                </style>
            </head>
            <body>
                <h1>{report.title}</h1>
                <p>{report.description}</p>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                    <tr>
                        <td>Total Tests</td>
                        <td>{report.test_count}</td>
                    </tr>
                    <tr>
                        <td>Passed</td>
                        <td>{report.passed_count}</td>
                    </tr>
                    <tr>
                        <td>Failed</td>
                        <td>{report.failed_count}</td>
                    </tr>
                    <tr>
                        <td>Success Rate</td>
                        <td>{report.success_rate}</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        return html
    
    @staticmethod
    def _generate_csv_report(report: Report) -> str:
        """Generate CSV report"""
        csv = f"""Report Title,{report.title}
Description,{report.description}
Generated At,{report.generated_at}

Metric,Value
Total Tests,{report.test_count}
Passed,{report.passed_count}
Failed,{report.failed_count}
Success Rate,{report.success_rate}
"""
        return csv
    
    @staticmethod
    def _generate_pdf_report(report: Report) -> str:
        """Generate PDF report (placeholder)"""
        return f"PDF Report: {report.title}"
