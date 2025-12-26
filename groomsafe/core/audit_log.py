"""
GROOMSAFE Audit Logging System
Ensures legal defensibility, accountability, and transparency
Immutable audit trail for all system decisions
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path
import json
from uuid import UUID

from .data_models import (
    AuditLogEntry,
    RiskAssessment,
    GroomingStage,
    RiskLevel
)


class AuditLogger:
    """
    Maintains comprehensive audit trail of all system actions
    Ensures legal defensibility and accountability
    """

    def __init__(self, log_directory: str = "./logs"):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)

        # Current session log file
        self.session_start = datetime.utcnow()
        self.session_log_file = self._get_session_log_file()

        # In-memory buffer for current session
        self.session_buffer: List[AuditLogEntry] = []

    def _get_session_log_file(self) -> Path:
        """Generate log file path for current session"""
        timestamp = self.session_start.strftime("%Y%m%d_%H%M%S")
        return self.log_directory / f"audit_log_{timestamp}.jsonl"

    def log_assessment_created(
        self,
        risk_assessment: RiskAssessment,
        conversation_id: UUID,
        model_version: str
    ):
        """
        Log creation of risk assessment

        Args:
            risk_assessment: Created risk assessment
            conversation_id: Conversation identifier
            model_version: Model version used
        """
        entry = AuditLogEntry(
            conversation_id=conversation_id,
            assessment_id=risk_assessment.assessment_id,
            action_type="assessment_created",
            actor="groomsafe_risk_scoring_engine",
            risk_score=risk_assessment.grooming_risk_score,
            risk_level=risk_assessment.risk_level,
            stage=risk_assessment.current_stage,
            decision_rationale=risk_assessment.reasoning_summary,
            model_version=model_version,
            metadata={
                'confidence': risk_assessment.confidence_level,
                'stage_confidence': risk_assessment.stage_confidence,
                'requires_review': risk_assessment.requires_human_review
            }
        )

        self._write_log_entry(entry)

    def log_human_review_triggered(
        self,
        conversation_id: UUID,
        assessment_id: UUID,
        trigger_reason: str,
        risk_score: float,
        risk_level: RiskLevel
    ):
        """
        Log when human review is triggered

        Args:
            conversation_id: Conversation identifier
            assessment_id: Assessment that triggered review
            trigger_reason: Reason for triggering review
            risk_score: Current risk score
            risk_level: Current risk level
        """
        entry = AuditLogEntry(
            conversation_id=conversation_id,
            assessment_id=assessment_id,
            action_type="human_review_triggered",
            actor="groomsafe_automated_triage",
            risk_score=risk_score,
            risk_level=risk_level,
            decision_rationale=trigger_reason,
            model_version="1.0.0"
        )

        self._write_log_entry(entry)

    def log_human_review_completed(
        self,
        conversation_id: UUID,
        assessment_id: UUID,
        reviewer_id: str,
        review_outcome: str,
        review_notes: str,
        action_taken: Optional[str] = None
    ):
        """
        Log completion of human review

        Args:
            conversation_id: Conversation identifier
            assessment_id: Assessment that was reviewed
            reviewer_id: Anonymous reviewer identifier
            review_outcome: Outcome of review (confirmed/dismissed/escalated)
            review_notes: Reviewer's notes
            action_taken: Action taken based on review
        """
        entry = AuditLogEntry(
            conversation_id=conversation_id,
            assessment_id=assessment_id,
            action_type="human_review_completed",
            actor=f"human_reviewer_{reviewer_id}",
            decision_rationale=review_notes,
            model_version="N/A",
            metadata={
                'review_outcome': review_outcome,
                'action_taken': action_taken,
                'review_duration': 'logged_separately'
            }
        )

        self._write_log_entry(entry)

    def log_intervention_action(
        self,
        conversation_id: UUID,
        assessment_id: Optional[UUID],
        intervention_type: str,
        intervention_details: str,
        actor: str
    ):
        """
        Log safety intervention action

        Args:
            conversation_id: Conversation identifier
            assessment_id: Related assessment (if any)
            intervention_type: Type of intervention (e.g., 'account_suspension')
            intervention_details: Details of intervention
            actor: Who/what initiated intervention
        """
        entry = AuditLogEntry(
            conversation_id=conversation_id,
            assessment_id=assessment_id,
            action_type=f"intervention_{intervention_type}",
            actor=actor,
            decision_rationale=intervention_details,
            model_version="N/A",
            metadata={
                'intervention_type': intervention_type
            }
        )

        self._write_log_entry(entry)

    def log_false_positive(
        self,
        conversation_id: UUID,
        assessment_id: UUID,
        reported_by: str,
        reason: str,
        original_risk_score: float
    ):
        """
        Log false positive report for model improvement

        Args:
            conversation_id: Conversation identifier
            assessment_id: Assessment that was false positive
            reported_by: Who reported the false positive
            reason: Reason it was false positive
            original_risk_score: Original risk score
        """
        entry = AuditLogEntry(
            conversation_id=conversation_id,
            assessment_id=assessment_id,
            action_type="false_positive_reported",
            actor=reported_by,
            risk_score=original_risk_score,
            decision_rationale=reason,
            model_version="1.0.0",
            metadata={
                'feedback_type': 'false_positive'
            }
        )

        self._write_log_entry(entry)

    def log_system_event(
        self,
        event_type: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log general system event

        Args:
            event_type: Type of system event
            description: Event description
            metadata: Additional event metadata
        """
        # Use a dummy UUID for system events
        from uuid import uuid4
        system_conv_id = uuid4()

        entry = AuditLogEntry(
            conversation_id=system_conv_id,
            action_type=f"system_{event_type}",
            actor="groomsafe_system",
            decision_rationale=description,
            model_version="1.0.0",
            metadata=metadata or {}
        )

        self._write_log_entry(entry)

    def _write_log_entry(self, entry: AuditLogEntry):
        """
        Write log entry to persistent storage

        Args:
            entry: AuditLogEntry to write
        """
        # Add to session buffer
        self.session_buffer.append(entry)

        # Write to JSONL file (append mode)
        with open(self.session_log_file, 'a') as f:
            json_data = entry.model_dump_json()
            f.write(json_data + '\n')

    def query_logs(
        self,
        conversation_id: Optional[UUID] = None,
        assessment_id: Optional[UUID] = None,
        action_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        risk_level: Optional[RiskLevel] = None
    ) -> List[AuditLogEntry]:
        """
        Query audit logs with filters

        Args:
            conversation_id: Filter by conversation
            assessment_id: Filter by assessment
            action_type: Filter by action type
            start_time: Filter by start timestamp
            end_time: Filter by end timestamp
            risk_level: Filter by risk level

        Returns:
            List of matching audit log entries
        """
        results = []

        # Query from all log files in directory
        for log_file in sorted(self.log_directory.glob("audit_log_*.jsonl")):
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        entry_data = json.loads(line)
                        entry = AuditLogEntry(**entry_data)

                        # Apply filters
                        if conversation_id and entry.conversation_id != conversation_id:
                            continue
                        if assessment_id and entry.assessment_id != assessment_id:
                            continue
                        if action_type and entry.action_type != action_type:
                            continue
                        if start_time and entry.timestamp < start_time:
                            continue
                        if end_time and entry.timestamp > end_time:
                            continue
                        if risk_level and entry.risk_level != risk_level:
                            continue

                        results.append(entry)

                    except Exception as e:
                        # Log parsing error but continue
                        print(f"Error parsing log entry: {e}")
                        continue

        return results

    def get_conversation_timeline(
        self,
        conversation_id: UUID
    ) -> List[AuditLogEntry]:
        """
        Get complete audit timeline for a conversation

        Args:
            conversation_id: Conversation identifier

        Returns:
            Chronologically sorted list of audit entries
        """
        entries = self.query_logs(conversation_id=conversation_id)
        return sorted(entries, key=lambda x: x.timestamp)

    def get_assessment_history(
        self,
        assessment_id: UUID
    ) -> List[AuditLogEntry]:
        """
        Get complete history for an assessment

        Args:
            assessment_id: Assessment identifier

        Returns:
            List of related audit entries
        """
        return self.query_logs(assessment_id=assessment_id)

    def generate_compliance_report(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Generate compliance report for date range

        Args:
            start_date: Report start date
            end_date: Report end date

        Returns:
            Dictionary with compliance metrics
        """
        entries = self.query_logs(start_time=start_date, end_time=end_date)

        # Calculate metrics
        total_assessments = len([
            e for e in entries if e.action_type == "assessment_created"
        ])

        risk_level_counts = {}
        for level in RiskLevel:
            risk_level_counts[level.value] = len([
                e for e in entries
                if e.risk_level == level and e.action_type == "assessment_created"
            ])

        human_reviews = len([
            e for e in entries if e.action_type == "human_review_triggered"
        ])

        interventions = len([
            e for e in entries if e.action_type.startswith("intervention_")
        ])

        false_positives = len([
            e for e in entries if e.action_type == "false_positive_reported"
        ])

        return {
            'report_period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'total_assessments': total_assessments,
            'risk_level_distribution': risk_level_counts,
            'human_reviews_triggered': human_reviews,
            'interventions_performed': interventions,
            'false_positives_reported': false_positives,
            'false_positive_rate': (
                false_positives / total_assessments
                if total_assessments > 0 else 0
            ),
            'human_review_rate': (
                human_reviews / total_assessments
                if total_assessments > 0 else 0
            )
        }

    def export_logs(
        self,
        output_file: Path,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        format: str = "jsonl"
    ):
        """
        Export audit logs for external analysis or archival

        Args:
            output_file: Output file path
            start_time: Optional start time filter
            end_time: Optional end time filter
            format: Export format (jsonl, json, csv)
        """
        entries = self.query_logs(start_time=start_time, end_time=end_time)

        if format == "jsonl":
            with open(output_file, 'w') as f:
                for entry in entries:
                    f.write(entry.model_dump_json() + '\n')

        elif format == "json":
            with open(output_file, 'w') as f:
                json.dump(
                    [entry.model_dump() for entry in entries],
                    f,
                    indent=2,
                    default=str
                )

        elif format == "csv":
            import csv
            with open(output_file, 'w', newline='') as f:
                if entries:
                    writer = csv.DictWriter(f, fieldnames=entries[0].model_dump().keys())
                    writer.writeheader()
                    for entry in entries:
                        writer.writerow(entry.model_dump())

    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get summary of current session

        Returns:
            Dictionary with session metrics
        """
        session_duration = (datetime.utcnow() - self.session_start).total_seconds() / 60.0

        action_counts = {}
        for entry in self.session_buffer:
            action_counts[entry.action_type] = action_counts.get(entry.action_type, 0) + 1

        return {
            'session_start': self.session_start.isoformat(),
            'session_duration_minutes': round(session_duration, 2),
            'total_log_entries': len(self.session_buffer),
            'action_type_counts': action_counts,
            'log_file': str(self.session_log_file)
        }
