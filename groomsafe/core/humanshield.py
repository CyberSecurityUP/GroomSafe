"""
HUMANSHIELD - Psychological Safety & Evidence Abstraction Layer
Protects investigators, moderators, and analysts from traumatic content
Provides safe, abstracted representations for decision-making
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict
import numpy as np

from .data_models import (
    Conversation,
    Message,
    RiskAssessment,
    BehavioralFeatures,
    HumanShieldSummary,
    SenderRole,
    GroomingStage
)


class ExposureLimitExceeded(Exception):
    """Raised when analyst exposure limits are exceeded"""
    pass


class HumanShieldLayer:
    """
    Abstraction layer for psychological safety
    Ensures investigators never see raw disturbing content
    """

    def __init__(self):
        # Exposure tracking (in production, would use persistent storage)
        self.analyst_exposure_tracker = defaultdict(lambda: {
            'session_start': datetime.utcnow(),
            'cases_reviewed': 0,
            'high_risk_exposures': 0,
            'total_exposure_minutes': 0
        })

        # Safety thresholds
        self.max_cases_per_session = 20
        self.max_high_risk_per_session = 5
        self.max_session_duration_minutes = 120
        self.mandatory_break_minutes = 15

    def create_safe_summary(
        self,
        conversation: Conversation,
        risk_assessment: RiskAssessment,
        features: BehavioralFeatures,
        exposure_level: str = "minimal"
    ) -> HumanShieldSummary:
        """
        Create analyst-safe summary of conversation

        Args:
            conversation: Original conversation
            risk_assessment: Risk assessment results
            features: Behavioral features
            exposure_level: Level of detail (minimal, moderate, detailed)

        Returns:
            HumanShieldSummary with abstracted, safe information
        """
        # Validate exposure level
        if exposure_level not in ["minimal", "moderate", "detailed"]:
            exposure_level = "minimal"

        # Calculate conversation metrics
        message_count = len(conversation.messages)
        duration_hours = self._calculate_duration(conversation)

        # Generate temporal pattern summary (abstract)
        temporal_summary = self._generate_temporal_summary(
            conversation, features
        )

        # Classify behavioral cluster
        behavioral_cluster = self._classify_behavioral_cluster(features)

        # Generate abstract risk indicators
        risk_indicators = self._generate_abstract_risk_indicators(
            features, risk_assessment
        )

        # Create timeline events (abstract, safe for visualization)
        timeline_events = self._create_timeline_events(
            conversation, features, risk_assessment, exposure_level
        )

        return HumanShieldSummary(
            conversation_id=conversation.conversation_id,
            message_count=message_count,
            conversation_duration_hours=duration_hours,
            temporal_pattern_summary=temporal_summary,
            behavioral_cluster=behavioral_cluster,
            key_risk_indicators=risk_indicators,
            timeline_events=timeline_events,
            exposure_level=exposure_level,
            analyst_safety_certified=True
        )

    def check_analyst_safety(
        self,
        analyst_id: str,
        risk_level: str
    ) -> Dict[str, Any]:
        """
        Check analyst exposure limits and enforce breaks

        Args:
            analyst_id: Unique analyst identifier
            risk_level: Risk level of case to review

        Returns:
            Dictionary with safety status and recommendations

        Raises:
            ExposureLimitExceeded: If analyst has exceeded safe limits
        """
        tracker = self.analyst_exposure_tracker[analyst_id]
        current_time = datetime.utcnow()

        # Calculate session duration
        session_duration = (
            current_time - tracker['session_start']
        ).total_seconds() / 60.0

        # Check session duration
        if session_duration > self.max_session_duration_minutes:
            return {
                'safe_to_proceed': False,
                'reason': 'Maximum session duration exceeded',
                'recommendation': f'Mandatory {self.mandatory_break_minutes}-minute break required',
                'cases_reviewed': tracker['cases_reviewed'],
                'session_duration_minutes': session_duration
            }

        # Check total cases
        if tracker['cases_reviewed'] >= self.max_cases_per_session:
            return {
                'safe_to_proceed': False,
                'reason': 'Maximum cases per session exceeded',
                'recommendation': f'Mandatory {self.mandatory_break_minutes}-minute break required',
                'cases_reviewed': tracker['cases_reviewed'],
                'session_duration_minutes': session_duration
            }

        # Check high-risk exposures
        if (risk_level in ['high', 'critical'] and
                tracker['high_risk_exposures'] >= self.max_high_risk_per_session):
            return {
                'safe_to_proceed': False,
                'reason': 'Maximum high-risk exposures exceeded',
                'recommendation': f'Mandatory {self.mandatory_break_minutes}-minute break required',
                'high_risk_exposures': tracker['high_risk_exposures'],
                'session_duration_minutes': session_duration
            }

        # Safe to proceed
        return {
            'safe_to_proceed': True,
            'cases_reviewed': tracker['cases_reviewed'],
            'high_risk_exposures': tracker['high_risk_exposures'],
            'session_duration_minutes': session_duration,
            'remaining_cases': self.max_cases_per_session - tracker['cases_reviewed']
        }

    def log_analyst_exposure(
        self,
        analyst_id: str,
        risk_level: str,
        exposure_duration_minutes: float
    ):
        """
        Log analyst exposure for tracking

        Args:
            analyst_id: Unique analyst identifier
            risk_level: Risk level of reviewed case
            exposure_duration_minutes: Time spent on case
        """
        tracker = self.analyst_exposure_tracker[analyst_id]
        tracker['cases_reviewed'] += 1
        tracker['total_exposure_minutes'] += exposure_duration_minutes

        if risk_level in ['high', 'critical']:
            tracker['high_risk_exposures'] += 1

    def reset_analyst_session(self, analyst_id: str):
        """Reset analyst session after break"""
        self.analyst_exposure_tracker[analyst_id] = {
            'session_start': datetime.utcnow(),
            'cases_reviewed': 0,
            'high_risk_exposures': 0,
            'total_exposure_minutes': 0
        }

    def _calculate_duration(self, conversation: Conversation) -> float:
        """Calculate conversation duration in hours"""
        if len(conversation.messages) < 2:
            return 0.0

        timestamps = [m.timestamp for m in conversation.messages]
        duration = (max(timestamps) - min(timestamps)).total_seconds() / 3600.0

        return round(duration, 2)

    def _generate_temporal_summary(
        self,
        conversation: Conversation,
        features: BehavioralFeatures
    ) -> str:
        """
        Generate abstract temporal pattern summary

        Returns:
            Safe, clinical description of temporal patterns
        """
        duration_hours = self._calculate_duration(conversation)
        message_count = len(conversation.messages)

        # Calculate messaging rate
        if duration_hours > 0:
            messages_per_hour = message_count / duration_hours
        else:
            messages_per_hour = 0

        # Classify temporal pattern
        if messages_per_hour > 10:
            intensity = "very high"
        elif messages_per_hour > 5:
            intensity = "high"
        elif messages_per_hour > 2:
            intensity = "moderate"
        else:
            intensity = "low"

        # Time irregularity
        if features.time_of_day_irregularity > 0.6:
            timing = "with significant off-hours activity"
        elif features.time_of_day_irregularity > 0.3:
            timing = "with some off-hours activity"
        else:
            timing = "during normal hours"

        return f"{intensity.capitalize()} messaging intensity ({messages_per_hour:.1f} msg/hr) over {duration_hours:.1f} hours, {timing}"

    def _classify_behavioral_cluster(self, features: BehavioralFeatures) -> str:
        """
        Classify conversation into behavioral cluster

        Returns:
            Abstract behavioral category (safe for analyst review)
        """
        # Calculate dominant behavioral patterns
        pattern_scores = {
            'High Contact Frequency': features.contact_frequency_score,
            'Persistence Pattern': features.persistence_after_nonresponse,
            'Temporal Anomaly': features.time_of_day_irregularity,
            'Emotional Manipulation': features.emotional_dependency_indicators,
            'Isolation Tactics': features.isolation_pressure,
            'Secrecy Pressure': features.secrecy_pressure,
            'Platform Migration': features.platform_migration_attempts,
            'Linguistic Shifts': features.tone_shift_score
        }

        # Get dominant pattern
        dominant_pattern = max(pattern_scores, key=pattern_scores.get)
        dominant_score = pattern_scores[dominant_pattern]

        if dominant_score < 0.3:
            return "Low Risk Behavioral Pattern"
        elif dominant_score < 0.6:
            return f"Moderate Risk: {dominant_pattern}"
        else:
            return f"High Risk: {dominant_pattern}"

    def _generate_abstract_risk_indicators(
        self,
        features: BehavioralFeatures,
        risk_assessment: RiskAssessment
    ) -> List[str]:
        """
        Generate list of abstract risk indicators

        Returns:
            List of safe, clinical risk indicator descriptions
        """
        indicators = []

        # Feature-based indicators (only include significant ones)
        if features.contact_frequency_score > 0.5:
            indicators.append("Escalating contact pattern detected")

        if features.persistence_after_nonresponse > 0.5:
            indicators.append("Persistent messaging despite non-response")

        if features.time_of_day_irregularity > 0.5:
            indicators.append("Off-hours messaging pattern")

        if features.emotional_dependency_indicators > 0.5:
            indicators.append("Emotional manipulation indicators")

        if features.isolation_pressure > 0.5:
            indicators.append("Isolation attempt signals")

        if features.secrecy_pressure > 0.5:
            indicators.append("Secrecy or privacy pressure")

        if features.platform_migration_attempts > 0.5:
            indicators.append("Platform migration attempts")

        # Stage-based indicator
        stage_descriptions = {
            GroomingStage.TRUST_BUILDING: "Trust building phase detected",
            GroomingStage.EMOTIONAL_DEPENDENCY: "Emotional dependency phase detected",
            GroomingStage.ISOLATION_ATTEMPTS: "Isolation attempt phase detected",
            GroomingStage.ESCALATION_RISK: "ESCALATION RISK PHASE DETECTED"
        }

        if risk_assessment.current_stage in stage_descriptions:
            indicators.append(stage_descriptions[risk_assessment.current_stage])

        return indicators if indicators else ["No significant risk indicators"]

    def _create_timeline_events(
        self,
        conversation: Conversation,
        features: BehavioralFeatures,
        risk_assessment: RiskAssessment,
        exposure_level: str
    ) -> List[Dict[str, Any]]:
        """
        Create abstracted timeline events for visualization

        Returns:
            List of timeline event dictionaries (safe for graphing)
        """
        events = []

        # Add conversation start event
        events.append({
            'timestamp': conversation.messages[0].timestamp.isoformat(),
            'event_type': 'conversation_start',
            'description': 'Initial contact',
            'risk_level': 'minimal'
        })

        # Add behavioral transition events based on message sequence
        # This is abstracted - no message content exposed
        messages = sorted(conversation.messages, key=lambda m: m.timestamp)

        # Sample events at key points (beginning, middle, end)
        if len(messages) >= 3:
            mid_point = len(messages) // 2

            # Middle event
            events.append({
                'timestamp': messages[mid_point].timestamp.isoformat(),
                'event_type': 'behavioral_shift',
                'description': 'Mid-conversation behavioral analysis point',
                'risk_level': self._get_risk_level_for_score(
                    risk_assessment.grooming_risk_score * 0.6
                )
            })

        # Add final assessment event
        events.append({
            'timestamp': conversation.messages[-1].timestamp.isoformat(),
            'event_type': 'risk_assessment',
            'description': f'Final risk score: {risk_assessment.grooming_risk_score:.1f}',
            'risk_level': risk_assessment.risk_level.value,
            'stage': risk_assessment.current_stage.value
        })

        # Add feature-based events (only for detailed exposure level)
        if exposure_level == 'detailed':
            if features.platform_migration_attempts > 0.6:
                # Add approximate timestamp for migration attempt
                events.append({
                    'timestamp': messages[-1].timestamp.isoformat(),
                    'event_type': 'platform_migration',
                    'description': 'Platform migration attempt detected',
                    'risk_level': 'high'
                })

        return events

    def _get_risk_level_for_score(self, score: float) -> str:
        """Map risk score to risk level string"""
        if score <= 20:
            return 'minimal'
        elif score <= 40:
            return 'low'
        elif score <= 60:
            return 'moderate'
        elif score <= 80:
            return 'high'
        else:
            return 'critical'

    def generate_visualization_data(
        self,
        conversation: Conversation,
        features: BehavioralFeatures,
        risk_assessment: RiskAssessment
    ) -> Dict[str, Any]:
        """
        Generate data for safe visualizations

        Returns:
            Dictionary with graph-ready data (no raw content)
        """
        return {
            'risk_score_gauge': {
                'score': risk_assessment.grooming_risk_score,
                'level': risk_assessment.risk_level.value,
                'confidence': risk_assessment.confidence_level
            },
            'feature_radar': {
                'contact_frequency': features.contact_frequency_score,
                'persistence': features.persistence_after_nonresponse,
                'time_irregularity': features.time_of_day_irregularity,
                'emotional_dependency': features.emotional_dependency_indicators,
                'isolation': features.isolation_pressure,
                'secrecy': features.secrecy_pressure,
                'platform_migration': features.platform_migration_attempts,
                'tone_shift': features.tone_shift_score
            },
            'temporal_heatmap': self._generate_temporal_heatmap(conversation),
            'stage_progression': {
                'current_stage': risk_assessment.current_stage.value,
                'confidence': risk_assessment.stage_confidence
            }
        }

    def _generate_temporal_heatmap(
        self,
        conversation: Conversation
    ) -> Dict[str, Any]:
        """
        Generate temporal heatmap data (abstract, safe)

        Returns:
            Heatmap data showing message distribution by time of day
        """
        hour_distribution = defaultdict(int)

        for msg in conversation.messages:
            if msg.sender_role == SenderRole.ADULT:
                hour_distribution[msg.timestamp.hour] += 1

        return {
            'hours': list(range(24)),
            'message_counts': [hour_distribution[h] for h in range(24)],
            'peak_hour': max(hour_distribution, key=hour_distribution.get) if hour_distribution else 12
        }
