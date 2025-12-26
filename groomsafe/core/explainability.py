"""
GROOMSAFE Explainability Module
Provides transparent, auditable explanations for risk assessments
Ensures legal defensibility and human understanding
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .data_models import (
    RiskAssessment,
    BehavioralFeatures,
    Conversation,
    FeatureContribution,
    GroomingStage
)


class ExplainabilityEngine:
    """
    Generates comprehensive explanations for risk assessments
    Answers: Why was this flagged? Which features contributed? How did risk evolve?
    """

    def __init__(self):
        self.model_version = "1.0.0"

    def generate_explanation(
        self,
        risk_assessment: RiskAssessment,
        features: BehavioralFeatures,
        conversation: Conversation
    ) -> Dict[str, Any]:
        """
        Generate comprehensive explanation for risk assessment

        Args:
            risk_assessment: Risk assessment to explain
            features: Behavioral features extracted
            conversation: Original conversation

        Returns:
            Dictionary with complete explanation data
        """
        explanation = {
            'assessment_id': str(risk_assessment.assessment_id),
            'conversation_id': str(risk_assessment.conversation_id),
            'timestamp': risk_assessment.assessment_timestamp.isoformat(),
            'model_version': self.model_version,

            # High-level summary
            'summary': self._generate_summary(risk_assessment),

            # Why was this flagged?
            'flagging_rationale': self._generate_flagging_rationale(
                risk_assessment, features
            ),

            # Feature contributions
            'feature_analysis': self._generate_feature_analysis(
                risk_assessment.feature_contributions
            ),

            # Stage analysis
            'stage_analysis': self._generate_stage_analysis(risk_assessment),

            # Risk evolution
            'risk_evolution': self._generate_risk_evolution(
                conversation, features, risk_assessment
            ),

            # Confidence factors
            'confidence_analysis': self._generate_confidence_analysis(
                risk_assessment, conversation
            ),

            # Recommended actions
            'recommendations': self._generate_recommendations(risk_assessment),

            # Limitations and caveats
            'limitations': self._generate_limitations()
        }

        return explanation

    def _generate_summary(self, risk_assessment: RiskAssessment) -> str:
        """Generate high-level summary of assessment"""
        return (
            f"Risk assessment classified as {risk_assessment.risk_level.value.upper()} "
            f"with score {risk_assessment.grooming_risk_score:.1f}/100 "
            f"(confidence: {risk_assessment.confidence_level:.2f}). "
            f"Conversation stage: {risk_assessment.current_stage.value.replace('_', ' ').title()}. "
            f"Human review {'IS REQUIRED' if risk_assessment.requires_human_review else 'not required'}."
        )

    def _generate_flagging_rationale(
        self,
        risk_assessment: RiskAssessment,
        features: BehavioralFeatures
    ) -> Dict[str, Any]:
        """
        Explain why this conversation was flagged

        Returns:
            Dictionary with flagging rationale
        """
        # Get primary reasons for flagging
        primary_reasons = []

        # Check risk score
        if risk_assessment.grooming_risk_score > 60:
            primary_reasons.append(
                f"High risk score ({risk_assessment.grooming_risk_score:.1f}/100) "
                f"exceeds safety threshold"
            )

        # Check stage
        if risk_assessment.current_stage in [
            GroomingStage.ISOLATION_ATTEMPTS,
            GroomingStage.ESCALATION_RISK
        ]:
            primary_reasons.append(
                f"Advanced grooming stage detected: "
                f"{risk_assessment.current_stage.value.replace('_', ' ').title()}"
            )

        # Check specific high-risk features
        high_risk_features = []
        feature_dict = {
            'Emotional dependency patterns': features.emotional_dependency_indicators,
            'Isolation pressure': features.isolation_pressure,
            'Secrecy pressure': features.secrecy_pressure,
            'Platform migration attempts': features.platform_migration_attempts,
            'Contact frequency escalation': features.contact_frequency_score,
            'Persistence after non-response': features.persistence_after_nonresponse
        }

        for feature_name, value in feature_dict.items():
            if value > 0.6:
                high_risk_features.append(f"{feature_name} ({value:.2f})")

        if high_risk_features:
            primary_reasons.append(
                f"High-risk behavioral patterns: {', '.join(high_risk_features)}"
            )

        return {
            'flagged': risk_assessment.grooming_risk_score > 40,
            'primary_reasons': primary_reasons if primary_reasons else [
                "Moderate behavioral signals warrant monitoring"
            ],
            'risk_level': risk_assessment.risk_level.value,
            'requires_action': risk_assessment.requires_human_review
        }

    def _generate_feature_analysis(
        self,
        feature_contributions: List[FeatureContribution]
    ) -> Dict[str, Any]:
        """
        Analyze and explain feature contributions

        Returns:
            Dictionary with feature analysis
        """
        # Sort by contribution weight
        sorted_features = sorted(
            feature_contributions,
            key=lambda x: x.contribution_weight,
            reverse=True
        )

        # Categorize features
        high_contributors = [
            f for f in sorted_features if f.contribution_weight > 0.1
        ]
        moderate_contributors = [
            f for f in sorted_features
            if 0.05 < f.contribution_weight <= 0.1
        ]
        low_contributors = [
            f for f in sorted_features if f.contribution_weight <= 0.05
        ]

        return {
            'top_contributors': [
                {
                    'feature': f.feature_name,
                    'value': f.value,
                    'contribution': f.contribution_weight,
                    'description': f.description
                }
                for f in high_contributors[:5]  # Top 5
            ],
            'moderate_contributors': [
                {
                    'feature': f.feature_name,
                    'value': f.value,
                    'contribution': f.contribution_weight
                }
                for f in moderate_contributors
            ],
            'feature_count': {
                'high': len(high_contributors),
                'moderate': len(moderate_contributors),
                'low': len(low_contributors)
            },
            'interpretation': self._interpret_feature_pattern(high_contributors)
        }

    def _interpret_feature_pattern(
        self,
        high_contributors: List[FeatureContribution]
    ) -> str:
        """Interpret pattern from high-contributing features"""
        if not high_contributors:
            return "No significant behavioral patterns detected"

        feature_names = [f.feature_name for f in high_contributors]

        # Pattern detection
        if 'emotional_dependency_indicators' in feature_names:
            if 'isolation_pressure' in feature_names:
                return "Pattern suggests emotional manipulation with isolation tactics"
            else:
                return "Pattern suggests emotional manipulation strategy"

        if 'platform_migration_attempts' in feature_names:
            if 'secrecy_pressure' in feature_names:
                return "Pattern suggests attempt to move conversation to private channels"

        if 'contact_frequency_score' in feature_names:
            if 'persistence_after_nonresponse' in feature_names:
                return "Pattern suggests escalating and persistent contact behavior"

        return "Multiple behavioral risk indicators detected"

    def _generate_stage_analysis(
        self,
        risk_assessment: RiskAssessment
    ) -> Dict[str, Any]:
        """
        Analyze and explain stage classification

        Returns:
            Dictionary with stage analysis
        """
        stage = risk_assessment.current_stage

        stage_descriptions = {
            GroomingStage.INITIAL_CONTACT: {
                'severity': 'low',
                'typical_duration': 'days to weeks',
                'next_stage': 'Trust Building',
                'watch_for': ['Increasing contact frequency', 'Personal questions']
            },
            GroomingStage.TRUST_BUILDING: {
                'severity': 'moderate',
                'typical_duration': 'weeks to months',
                'next_stage': 'Emotional Dependency',
                'watch_for': ['Emotional manipulation', 'Isolation attempts']
            },
            GroomingStage.EMOTIONAL_DEPENDENCY: {
                'severity': 'high',
                'typical_duration': 'variable',
                'next_stage': 'Isolation Attempts',
                'watch_for': ['Secrecy requests', 'Platform migration']
            },
            GroomingStage.ISOLATION_ATTEMPTS: {
                'severity': 'critical',
                'typical_duration': 'variable',
                'next_stage': 'Escalation Risk',
                'watch_for': ['Off-platform contact', 'Meeting requests']
            },
            GroomingStage.ESCALATION_RISK: {
                'severity': 'critical',
                'typical_duration': 'immediate',
                'next_stage': 'None (intervention required)',
                'watch_for': ['All escalation indicators']
            }
        }

        stage_info = stage_descriptions.get(stage, {
            'severity': 'unknown',
            'typical_duration': 'unknown',
            'next_stage': 'unknown',
            'watch_for': []
        })

        return {
            'current_stage': stage.value.replace('_', ' ').title(),
            'stage_confidence': risk_assessment.stage_confidence,
            'severity': stage_info['severity'],
            'typical_duration': stage_info['typical_duration'],
            'potential_next_stage': stage_info['next_stage'],
            'warning_signs': stage_info['watch_for']
        }

    def _generate_risk_evolution(
        self,
        conversation: Conversation,
        features: BehavioralFeatures,
        risk_assessment: RiskAssessment
    ) -> Dict[str, Any]:
        """
        Explain how risk evolved over time

        Returns:
            Dictionary with risk evolution analysis
        """
        duration_hours = 0
        if len(conversation.messages) > 1:
            timestamps = [m.timestamp for m in conversation.messages]
            duration_hours = (
                max(timestamps) - min(timestamps)
            ).total_seconds() / 3600.0

        # Estimate risk progression
        progression_rate = "unknown"
        if duration_hours > 0:
            if duration_hours < 24:
                progression_rate = "rapid (less than 24 hours)"
            elif duration_hours < 168:  # 1 week
                progression_rate = "moderate (days)"
            else:
                progression_rate = "gradual (weeks or more)"

        return {
            'conversation_duration_hours': round(duration_hours, 2),
            'message_count': len(conversation.messages),
            'progression_rate': progression_rate,
            'risk_trajectory': self._assess_trajectory(
                risk_assessment.grooming_risk_score
            ),
            'timeline_summary': (
                f"Conversation spanned {duration_hours:.1f} hours with "
                f"{len(conversation.messages)} messages, "
                f"reaching {risk_assessment.current_stage.value.replace('_', ' ')} stage"
            )
        }

    def _assess_trajectory(self, risk_score: float) -> str:
        """Assess risk trajectory based on score"""
        if risk_score < 30:
            return "stable at low risk"
        elif risk_score < 60:
            return "increasing to moderate risk"
        elif risk_score < 80:
            return "escalating to high risk"
        else:
            return "critical escalation"

    def _generate_confidence_analysis(
        self,
        risk_assessment: RiskAssessment,
        conversation: Conversation
    ) -> Dict[str, Any]:
        """
        Explain confidence level in assessment

        Returns:
            Dictionary with confidence analysis
        """
        confidence = risk_assessment.confidence_level
        message_count = len(conversation.messages)

        # Factors affecting confidence
        factors = []

        if message_count < 5:
            factors.append("Limited data (few messages)")
        elif message_count > 20:
            factors.append("Sufficient data (many messages)")

        if confidence > 0.7:
            confidence_label = "high"
        elif confidence > 0.5:
            confidence_label = "moderate"
        else:
            confidence_label = "low"

        return {
            'confidence_score': confidence,
            'confidence_label': confidence_label,
            'factors': factors,
            'reliability': (
                "High confidence assessments are more reliable for decision-making. "
                "Low confidence assessments may require additional data or human review."
            )
        }

    def _generate_recommendations(
        self,
        risk_assessment: RiskAssessment
    ) -> List[str]:
        """Generate action recommendations based on assessment"""
        recommendations = []

        # Risk-based recommendations
        if risk_assessment.grooming_risk_score >= 80:
            recommendations.extend([
                "URGENT: Immediate human review required",
                "Escalate to platform safety team",
                "Consider emergency intervention protocols",
                "Preserve all evidence for potential investigation",
                "Activate victim support resources"
            ])
        elif risk_assessment.grooming_risk_score >= 60:
            recommendations.extend([
                "High-priority human review required within 24 hours",
                "Consider platform-level safety interventions",
                "Monitor for escalation patterns",
                "Prepare support resources"
            ])
        elif risk_assessment.grooming_risk_score >= 40:
            recommendations.extend([
                "Increased monitoring recommended",
                "Track feature progression over time",
                "Consider educational interventions"
            ])
        else:
            recommendations.extend([
                "Continue baseline monitoring",
                "Track for pattern changes"
            ])

        # Stage-based recommendations
        stage_recs = {
            GroomingStage.ESCALATION_RISK: [
                "CRITICAL: Immediate action required"
            ],
            GroomingStage.ISOLATION_ATTEMPTS: [
                "Alert platform safety team",
                "Document evidence for investigation"
            ]
        }

        if risk_assessment.current_stage in stage_recs:
            recommendations.extend(stage_recs[risk_assessment.current_stage])

        return recommendations

    def _generate_limitations(self) -> List[str]:
        """Document system limitations and caveats"""
        return [
            "This is a risk signaling system, not a criminal accusation tool",
            "False positives are possible; human review is essential",
            "System analyzes behavioral patterns, not content semantics",
            "Effectiveness depends on data quality and completeness",
            "Cultural and contextual factors may not be fully captured",
            "System is designed as one component of comprehensive safety measures",
            "Regular model updates and validation are required for accuracy"
        ]

    def generate_audit_report(
        self,
        risk_assessment: RiskAssessment,
        features: BehavioralFeatures,
        conversation: Conversation
    ) -> str:
        """
        Generate formal audit report for legal/compliance purposes

        Returns:
            Formatted audit report as string
        """
        explanation = self.generate_explanation(
            risk_assessment, features, conversation
        )

        report_lines = [
            "=" * 80,
            "GROOMSAFE RISK ASSESSMENT AUDIT REPORT",
            "=" * 80,
            "",
            f"Assessment ID: {risk_assessment.assessment_id}",
            f"Conversation ID: {risk_assessment.conversation_id}",
            f"Timestamp: {risk_assessment.assessment_timestamp.isoformat()}",
            f"Model Version: {self.model_version}",
            "",
            "-" * 80,
            "SUMMARY",
            "-" * 80,
            explanation['summary'],
            "",
            "-" * 80,
            "RISK METRICS",
            "-" * 80,
            f"Risk Score: {risk_assessment.grooming_risk_score:.2f}/100",
            f"Risk Level: {risk_assessment.risk_level.value.upper()}",
            f"Confidence: {risk_assessment.confidence_level:.2f}",
            f"Stage: {risk_assessment.current_stage.value.replace('_', ' ').title()}",
            f"Stage Confidence: {risk_assessment.stage_confidence:.2f}",
            "",
            "-" * 80,
            "PRIMARY RISK FACTORS",
            "-" * 80,
        ]

        for reason in explanation['flagging_rationale']['primary_reasons']:
            report_lines.append(f"- {reason}")

        report_lines.extend([
            "",
            "-" * 80,
            "TOP CONTRIBUTING FEATURES",
            "-" * 80,
        ])

        for contrib in explanation['feature_analysis']['top_contributors']:
            report_lines.append(
                f"- {contrib['feature']}: {contrib['value']:.3f} "
                f"(contribution: {contrib['contribution']:.3f})"
            )
            report_lines.append(f"  {contrib['description']}")

        report_lines.extend([
            "",
            "-" * 80,
            "RECOMMENDATIONS",
            "-" * 80,
        ])

        for rec in explanation['recommendations']:
            report_lines.append(f"- {rec}")

        report_lines.extend([
            "",
            "-" * 80,
            "LIMITATIONS",
            "-" * 80,
        ])

        for limitation in explanation['limitations']:
            report_lines.append(f"- {limitation}")

        report_lines.extend([
            "",
            "=" * 80,
            "END OF REPORT",
            "=" * 80
        ])

        return "\n".join(report_lines)
