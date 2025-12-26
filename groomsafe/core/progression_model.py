"""
GROOMSAFE Progression Model
Stage-based grooming progression detection
Abstract, non-sexual, time-aware classification
"""

from typing import Tuple
import numpy as np

from .data_models import (
    BehavioralFeatures,
    GroomingStage,
    Conversation
)


class GroomingProgressionModel:
    """
    Classifies conversation progression through grooming stages
    Based on behavioral feature patterns and temporal analysis
    """

    def __init__(self):
        # Define thresholds for stage classification
        # These are research-based heuristics and should be tuned with real data

        # Initial Contact: Minimal behavioral signals
        self.initial_contact_threshold = 0.2

        # Trust Building: Low-moderate contact frequency, minimal pressure
        self.trust_building_threshold = 0.35

        # Emotional Dependency: Emotional indicators elevated
        self.emotional_dependency_threshold = 0.50

        # Isolation Attempts: Isolation and secrecy signals present
        self.isolation_threshold = 0.65

        # Escalation Risk: Multiple high-risk signals active
        self.escalation_threshold = 0.75

    def classify_stage(
        self,
        features: BehavioralFeatures,
        conversation: Conversation
    ) -> Tuple[GroomingStage, float]:
        """
        Classify conversation into grooming progression stage

        Args:
            features: Extracted behavioral features
            conversation: Original conversation (for temporal context)

        Returns:
            Tuple of (GroomingStage, confidence_score)
        """
        # Calculate composite risk indicators for each stage
        stage_scores = self._calculate_stage_scores(features)

        # Determine most likely stage based on feature patterns
        stage, confidence = self._determine_stage(stage_scores, features)

        return stage, confidence

    def _calculate_stage_scores(self, features: BehavioralFeatures) -> dict:
        """
        Calculate score for each potential stage based on feature patterns

        Returns:
            Dictionary mapping GroomingStage to score
        """
        scores = {}

        # Initial Contact Stage
        # Characteristics: Low behavioral signals, exploratory contact
        initial_score = self._score_initial_contact(features)
        scores[GroomingStage.INITIAL_CONTACT] = initial_score

        # Trust Building Stage
        # Characteristics: Increasing contact, minimal pressure, friendly tone
        trust_score = self._score_trust_building(features)
        scores[GroomingStage.TRUST_BUILDING] = trust_score

        # Emotional Dependency Stage
        # Characteristics: Emotional manipulation, dependency building
        dependency_score = self._score_emotional_dependency(features)
        scores[GroomingStage.EMOTIONAL_DEPENDENCY] = dependency_score

        # Isolation Attempts Stage
        # Characteristics: Secrecy, isolation pressure, platform migration
        isolation_score = self._score_isolation_attempts(features)
        scores[GroomingStage.ISOLATION_ATTEMPTS] = isolation_score

        # Escalation Risk Stage
        # Characteristics: Multiple high-risk signals, urgent patterns
        escalation_score = self._score_escalation_risk(features)
        scores[GroomingStage.ESCALATION_RISK] = escalation_score

        return scores

    def _score_initial_contact(self, features: BehavioralFeatures) -> float:
        """
        Score for Initial Contact stage
        Low behavioral signals, exploratory communication
        """
        # Initial contact characterized by LOW scores across all features
        avg_feature_score = self._calculate_average_features(features)

        # Inverse relationship: lower features = higher initial contact score
        if avg_feature_score < self.initial_contact_threshold:
            return 1.0 - (avg_feature_score / self.initial_contact_threshold)
        else:
            return 0.0

    def _score_trust_building(self, features: BehavioralFeatures) -> float:
        """
        Score for Trust Building stage
        Moderate contact frequency, low pressure tactics
        """
        # Trust building: moderate contact, low isolation/secrecy
        contact_component = features.contact_frequency_score * 0.4
        emotional_component = features.emotional_dependency_indicators * 0.3
        tone_component = features.tone_shift_score * 0.3

        # Low isolation/secrecy pressure
        pressure_penalty = (
            features.isolation_pressure +
            features.secrecy_pressure
        ) / 2.0

        # High trust building when moderate contact/emotional, low pressure
        trust_score = (contact_component + emotional_component + tone_component)
        trust_score = trust_score * (1.0 - pressure_penalty * 0.5)

        # Peak in middle range
        if 0.2 < trust_score < 0.5:
            return trust_score * 2.0  # Amplify scores in this range
        else:
            return trust_score * 0.5

    def _score_emotional_dependency(self, features: BehavioralFeatures) -> float:
        """
        Score for Emotional Dependency stage
        High emotional manipulation, increasing contact
        """
        # Primary indicators
        emotional_weight = features.emotional_dependency_indicators * 0.5
        contact_weight = features.contact_frequency_score * 0.25
        persistence_weight = features.persistence_after_nonresponse * 0.25

        dependency_score = emotional_weight + contact_weight + persistence_weight

        return float(np.clip(dependency_score, 0.0, 1.0))

    def _score_isolation_attempts(self, features: BehavioralFeatures) -> float:
        """
        Score for Isolation Attempts stage
        Secrecy pressure, isolation tactics, platform migration
        """
        # Primary indicators
        isolation_weight = features.isolation_pressure * 0.35
        secrecy_weight = features.secrecy_pressure * 0.35
        migration_weight = features.platform_migration_attempts * 0.30

        isolation_score = isolation_weight + secrecy_weight + migration_weight

        return float(np.clip(isolation_score, 0.0, 1.0))

    def _score_escalation_risk(self, features: BehavioralFeatures) -> float:
        """
        Score for Escalation Risk stage
        Multiple high-risk signals, urgent/persistent patterns
        """
        # Escalation indicated by multiple elevated features
        high_risk_features = [
            features.contact_frequency_score,
            features.persistence_after_nonresponse,
            features.time_of_day_irregularity,
            features.emotional_dependency_indicators,
            features.isolation_pressure,
            features.secrecy_pressure,
            features.platform_migration_attempts
        ]

        # Count features above high-risk threshold
        high_risk_count = sum(1 for f in high_risk_features if f > 0.6)

        # Calculate average of high-risk features
        avg_high_risk = np.mean([f for f in high_risk_features if f > 0.5]) if any(
            f > 0.5 for f in high_risk_features) else 0.0

        # Escalation score based on both count and intensity
        escalation_score = (
            (high_risk_count / len(high_risk_features)) * 0.5 +
            avg_high_risk * 0.5
        )

        return float(np.clip(escalation_score, 0.0, 1.0))

    def _determine_stage(
        self,
        stage_scores: dict,
        features: BehavioralFeatures
    ) -> Tuple[GroomingStage, float]:
        """
        Determine most likely stage from scores

        Args:
            stage_scores: Dictionary of stage scores
            features: Original features (for tie-breaking)

        Returns:
            Tuple of (GroomingStage, confidence)
        """
        # Find stage with highest score
        max_stage = max(stage_scores, key=stage_scores.get)
        max_score = stage_scores[max_stage]

        # Calculate confidence based on separation from other stages
        sorted_scores = sorted(stage_scores.values(), reverse=True)

        if len(sorted_scores) > 1:
            # Confidence based on margin between top two scores
            margin = sorted_scores[0] - sorted_scores[1]
            confidence = min(max_score + margin * 0.5, 1.0)
        else:
            confidence = max_score

        # Apply minimum confidence threshold
        confidence = max(confidence, 0.1)

        # Handle edge case: if all scores very low, classify as INITIAL_CONTACT
        if max_score < 0.15:
            return GroomingStage.INITIAL_CONTACT, 0.5

        return max_stage, float(np.clip(confidence, 0.0, 1.0))

    def _calculate_average_features(self, features: BehavioralFeatures) -> float:
        """Calculate average of all feature scores"""
        feature_values = [
            features.contact_frequency_score,
            features.persistence_after_nonresponse,
            features.time_of_day_irregularity,
            features.emotional_dependency_indicators,
            features.isolation_pressure,
            features.secrecy_pressure,
            features.platform_migration_attempts,
            features.tone_shift_score
        ]

        return float(np.mean(feature_values))

    def get_stage_description(self, stage: GroomingStage) -> str:
        """
        Get human-readable description of a grooming stage

        Args:
            stage: GroomingStage enum value

        Returns:
            Description string
        """
        descriptions = {
            GroomingStage.INITIAL_CONTACT: (
                "Initial contact phase with minimal behavioral signals. "
                "Conversation appears exploratory with low risk indicators."
            ),
            GroomingStage.TRUST_BUILDING: (
                "Trust building phase characterized by increasing contact frequency "
                "and developing rapport. Moderate behavioral signals present."
            ),
            GroomingStage.EMOTIONAL_DEPENDENCY: (
                "Emotional dependency phase with patterns suggesting emotional "
                "manipulation or dependency building. Elevated risk indicators."
            ),
            GroomingStage.ISOLATION_ATTEMPTS: (
                "Isolation attempt phase showing secrecy pressure, isolation tactics, "
                "or platform migration attempts. High risk indicators present."
            ),
            GroomingStage.ESCALATION_RISK: (
                "Escalation risk phase with multiple high-risk behavioral signals. "
                "Urgent patterns detected requiring immediate review."
            ),
            GroomingStage.UNKNOWN: (
                "Unable to classify stage due to insufficient data or "
                "ambiguous patterns."
            )
        }

        return descriptions.get(stage, "No description available")

    def get_stage_recommendations(self, stage: GroomingStage) -> list:
        """
        Get recommended actions for each stage

        Args:
            stage: GroomingStage enum value

        Returns:
            List of recommended actions
        """
        recommendations = {
            GroomingStage.INITIAL_CONTACT: [
                "Continue monitoring conversation patterns",
                "Establish baseline behavioral metrics",
                "No immediate intervention required"
            ],
            GroomingStage.TRUST_BUILDING: [
                "Increased monitoring recommended",
                "Track feature progression over time",
                "Consider educational interventions for potential victim"
            ],
            GroomingStage.EMOTIONAL_DEPENDENCY: [
                "High-priority monitoring required",
                "Human review recommended within 24 hours",
                "Consider platform-level safety interventions",
                "Prepare support resources for potential victim"
            ],
            GroomingStage.ISOLATION_ATTEMPTS: [
                "Urgent human review required",
                "Consider immediate safety interventions",
                "Alert platform safety team",
                "Document evidence for potential investigation"
            ],
            GroomingStage.ESCALATION_RISK: [
                "CRITICAL: Immediate human review required",
                "Escalate to platform safety team immediately",
                "Consider emergency intervention protocols",
                "Preserve all evidence for law enforcement",
                "Activate victim support resources"
            ],
            GroomingStage.UNKNOWN: [
                "Gather additional data for classification",
                "Manual review may be required",
                "Continue baseline monitoring"
            ]
        }

        return recommendations.get(stage, [])
