"""
GROOMSAFE Risk Scoring Engine
Produces explainable, auditable risk assessments
Signals risk without assigning guilt
"""

from typing import List
import numpy as np

from .data_models import (
    BehavioralFeatures,
    RiskAssessment,
    FeatureContribution,
    GroomingStage,
    Conversation,
    RiskLevel
)
from .feature_extraction import BehavioralFeatureExtractor
from .progression_model import GroomingProgressionModel


class RiskScoringEngine:
    """
    Combines behavioral features and progression analysis
    to produce comprehensive risk assessments
    """

    def __init__(self):
        self.feature_extractor = BehavioralFeatureExtractor()
        self.progression_model = GroomingProgressionModel()

        # Feature weights for risk calculation
        # These can be tuned based on research and real-world validation
        # Higher weights on critical indicators (secrecy, isolation, emotional dependency)
        self.feature_weights = {
            'contact_frequency_score': 0.10,
            'persistence_after_nonresponse': 0.13,
            'time_of_day_irregularity': 0.08,
            'emotional_dependency_indicators': 0.22,  # Increased (manipulation)
            'isolation_pressure': 0.20,  # Increased (critical warning sign)
            'secrecy_pressure': 0.18,  # Increased (critical warning sign)
            'platform_migration_attempts': 0.06,
            'tone_shift_score': 0.03
        }

        # Stage-based risk multipliers
        # Adjusted to better reflect progression severity
        self.stage_multipliers = {
            GroomingStage.INITIAL_CONTACT: 0.4,  # Slightly increased from 0.3
            GroomingStage.TRUST_BUILDING: 0.6,  # Increased from 0.5
            GroomingStage.EMOTIONAL_DEPENDENCY: 0.8,  # Increased from 0.7
            GroomingStage.ISOLATION_ATTEMPTS: 0.95,  # Increased from 0.85
            GroomingStage.ESCALATION_RISK: 1.2,  # Can exceed 1.0 for critical cases
            GroomingStage.UNKNOWN: 0.5  # Increased from 0.4
        }

        # Human review thresholds
        self.human_review_threshold = 60.0  # Risk score requiring review
        self.critical_threshold = 80.0  # Critical risk requiring immediate review

    def assess_risk(self, conversation: Conversation) -> RiskAssessment:
        """
        Perform comprehensive risk assessment on conversation

        Args:
            conversation: Conversation object to assess

        Returns:
            RiskAssessment object with scores, stage, and explanations
        """
        # Extract behavioral features
        features = self.feature_extractor.extract_features(conversation)

        # Classify progression stage
        stage, stage_confidence = self.progression_model.classify_stage(
            features, conversation
        )

        # Calculate base risk score from features
        base_risk_score = self._calculate_base_risk(features)

        # Apply stage multiplier
        stage_multiplier = self.stage_multipliers[stage]
        adjusted_risk_score = base_risk_score * stage_multiplier

        # Calculate final risk score (0-100 scale)
        final_risk_score = min(adjusted_risk_score * 100, 100.0)

        # Calculate overall confidence
        confidence = self._calculate_confidence(
            features, stage_confidence, conversation
        )

        # Generate feature contributions for explainability
        feature_contributions = self._generate_feature_contributions(
            features, stage_multiplier
        )

        # Generate reasoning summary
        reasoning_summary = self._generate_reasoning(
            final_risk_score, stage, features, conversation
        )

        # Determine if human review required
        requires_review = self._requires_human_review(
            final_risk_score, stage, confidence
        )

        # Create risk assessment
        assessment = RiskAssessment(
            conversation_id=conversation.conversation_id,
            grooming_risk_score=final_risk_score,
            confidence_level=confidence,
            risk_level=self._determine_risk_level(final_risk_score),
            current_stage=stage,
            stage_confidence=stage_confidence,
            feature_contributions=feature_contributions,
            reasoning_summary=reasoning_summary,
            requires_human_review=requires_review
        )

        return assessment

    def _calculate_base_risk(self, features: BehavioralFeatures) -> float:
        """
        Calculate base risk score from weighted features

        Args:
            features: Extracted behavioral features

        Returns:
            Base risk score (0.0 to 1.0)
        """
        weighted_score = 0.0

        # Apply weights to each feature
        feature_dict = {
            'contact_frequency_score': features.contact_frequency_score,
            'persistence_after_nonresponse': features.persistence_after_nonresponse,
            'time_of_day_irregularity': features.time_of_day_irregularity,
            'emotional_dependency_indicators': features.emotional_dependency_indicators,
            'isolation_pressure': features.isolation_pressure,
            'secrecy_pressure': features.secrecy_pressure,
            'platform_migration_attempts': features.platform_migration_attempts,
            'tone_shift_score': features.tone_shift_score
        }

        for feature_name, feature_value in feature_dict.items():
            weight = self.feature_weights.get(feature_name, 0.0)
            weighted_score += feature_value * weight

        # Synergy boost: When multiple critical features are high simultaneously
        # This reflects that combined indicators are more concerning
        critical_features = [
            features.emotional_dependency_indicators,
            features.isolation_pressure,
            features.secrecy_pressure
        ]

        # Count how many critical features are above threshold (0.5)
        high_critical_count = sum(1 for f in critical_features if f > 0.5)

        # Apply synergy boost if 2 or 3 critical features are high
        if high_critical_count >= 2:
            synergy_boost = 0.15 * (high_critical_count - 1)  # 0.15 for 2, 0.30 for 3
            weighted_score = min(weighted_score + synergy_boost, 1.0)

        return float(np.clip(weighted_score, 0.0, 1.0))

    def _calculate_confidence(
        self,
        features: BehavioralFeatures,
        stage_confidence: float,
        conversation: Conversation
    ) -> float:
        """
        Calculate confidence in the risk assessment

        Factors:
        - Number of messages (more data = higher confidence)
        - Feature consistency
        - Stage classification confidence

        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Data quantity factor
        message_count = len(conversation.messages)
        if message_count < 5:
            data_confidence = 0.3
        elif message_count < 10:
            data_confidence = 0.5
        elif message_count < 20:
            data_confidence = 0.7
        else:
            data_confidence = 0.9

        # Feature consistency factor (variance in feature values)
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

        # Lower variance in high-risk features = higher confidence
        feature_variance = np.var(feature_values)
        consistency_confidence = 1.0 - min(feature_variance, 0.5) * 2

        # Combined confidence
        overall_confidence = (
            data_confidence * 0.4 +
            stage_confidence * 0.3 +
            consistency_confidence * 0.3
        )

        return float(np.clip(overall_confidence, 0.0, 1.0))

    def _generate_feature_contributions(
        self,
        features: BehavioralFeatures,
        stage_multiplier: float
    ) -> List[FeatureContribution]:
        """
        Generate detailed feature contributions for explainability

        Args:
            features: Extracted behavioral features
            stage_multiplier: Stage-based risk multiplier

        Returns:
            List of FeatureContribution objects
        """
        contributions = []

        feature_data = {
            'contact_frequency_score': (
                features.contact_frequency_score,
                "Escalation in contact frequency over time"
            ),
            'persistence_after_nonresponse': (
                features.persistence_after_nonresponse,
                "Continued messaging despite non-response"
            ),
            'time_of_day_irregularity': (
                features.time_of_day_irregularity,
                "Messaging at unusual hours"
            ),
            'emotional_dependency_indicators': (
                features.emotional_dependency_indicators,
                "Patterns suggesting emotional manipulation"
            ),
            'isolation_pressure': (
                features.isolation_pressure,
                "Attempts to isolate target from others"
            ),
            'secrecy_pressure': (
                features.secrecy_pressure,
                "Requests for secrecy or privacy"
            ),
            'platform_migration_attempts': (
                features.platform_migration_attempts,
                "Attempts to move conversation to other platforms"
            ),
            'tone_shift_score': (
                features.tone_shift_score,
                "Changes in linguistic tone over time"
            )
        }

        for feature_name, (value, description) in feature_data.items():
            weight = self.feature_weights.get(feature_name, 0.0)
            contribution_weight = value * weight * stage_multiplier

            contributions.append(FeatureContribution(
                feature_name=feature_name,
                value=value,
                contribution_weight=contribution_weight,
                description=description
            ))

        # Sort by contribution weight (highest first)
        contributions.sort(key=lambda x: x.contribution_weight, reverse=True)

        return contributions

    def _generate_reasoning(
        self,
        risk_score: float,
        stage: GroomingStage,
        features: BehavioralFeatures,
        conversation: Conversation
    ) -> str:
        """
        Generate human-readable explanation of risk assessment

        Args:
            risk_score: Final risk score
            stage: Classified grooming stage
            features: Behavioral features
            conversation: Original conversation

        Returns:
            Reasoning summary string
        """
        # Start with stage description
        stage_desc = self.progression_model.get_stage_description(stage)

        # Identify top risk factors
        feature_dict = {
            'Contact frequency escalation': features.contact_frequency_score,
            'Persistence after non-response': features.persistence_after_nonresponse,
            'Unusual messaging hours': features.time_of_day_irregularity,
            'Emotional dependency patterns': features.emotional_dependency_indicators,
            'Isolation pressure': features.isolation_pressure,
            'Secrecy requests': features.secrecy_pressure,
            'Platform migration attempts': features.platform_migration_attempts,
            'Tone shifts': features.tone_shift_score
        }

        # Get top 3 contributing factors
        top_factors = sorted(
            feature_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        top_factors_text = ", ".join([
            f"{name} ({value:.2f})"
            for name, value in top_factors if value > 0.3
        ])

        # Construct reasoning
        reasoning_parts = [
            f"Risk Score: {risk_score:.1f}/100",
            f"Classification: {stage.value.replace('_', ' ').title()}",
            stage_desc,
            f"Message Count: {len(conversation.messages)}",
        ]

        if top_factors_text:
            reasoning_parts.append(f"Primary Risk Factors: {top_factors_text}")

        return " | ".join(reasoning_parts)

    def _requires_human_review(
        self,
        risk_score: float,
        stage: GroomingStage,
        confidence: float
    ) -> bool:
        """
        Determine if human review is required

        Args:
            risk_score: Final risk score
            stage: Classified stage
            confidence: Confidence level

        Returns:
            Boolean indicating if human review required
        """
        # Always require review for critical risk
        if risk_score >= self.critical_threshold:
            return True

        # Require review for high risk scores
        if risk_score >= self.human_review_threshold:
            return True

        # Require review for escalation stage regardless of score
        if stage == GroomingStage.ESCALATION_RISK:
            return True

        # Require review for isolation stage with moderate confidence
        if stage == GroomingStage.ISOLATION_ATTEMPTS and confidence > 0.5:
            return True

        return False

    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """Map risk score to risk level enum"""
        if risk_score <= 20:
            return RiskLevel.MINIMAL
        elif risk_score <= 40:
            return RiskLevel.LOW
        elif risk_score <= 60:
            return RiskLevel.MODERATE
        elif risk_score <= 80:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
