"""
GROOMSAFE Feature Extraction
Behavioral pattern analysis without content inspection
Focuses on temporal, relational, and behavioral signals
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import numpy as np
from collections import Counter

from .data_models import Conversation, Message, BehavioralFeatures, SenderRole


class BehavioralFeatureExtractor:
    """
    Extracts behavioral features from conversation sequences
    No keyword analysis, no explicit content processing
    """

    def __init__(self):
        # Define normal messaging hours (9 AM - 9 PM)
        self.normal_hour_start = 9
        self.normal_hour_end = 21

        # Response time thresholds (in hours)
        self.non_response_threshold = 24.0

    def extract_features(self, conversation: Conversation) -> BehavioralFeatures:
        """
        Extract all behavioral features from a conversation

        Args:
            conversation: Conversation object with message sequence

        Returns:
            BehavioralFeatures object with extracted signals
        """
        messages = conversation.messages

        if len(messages) < 2:
            # Insufficient data for meaningful analysis
            return self._minimal_features(conversation.conversation_id)

        # Extract individual feature components
        contact_frequency = self._calculate_contact_frequency(messages)
        persistence = self._calculate_persistence(messages)
        time_irregularity = self._calculate_time_irregularity(messages)
        emotional_dependency = self._calculate_emotional_dependency(messages)
        isolation = self._calculate_isolation_pressure(messages)
        secrecy = self._calculate_secrecy_pressure(messages)
        platform_migration = self._calculate_platform_migration(messages)
        tone_shift = self._calculate_tone_shift(messages)

        return BehavioralFeatures(
            conversation_id=conversation.conversation_id,
            contact_frequency_score=contact_frequency,
            persistence_after_nonresponse=persistence,
            time_of_day_irregularity=time_irregularity,
            emotional_dependency_indicators=emotional_dependency,
            isolation_pressure=isolation,
            secrecy_pressure=secrecy,
            platform_migration_attempts=platform_migration,
            tone_shift_score=tone_shift
        )

    def _minimal_features(self, conversation_id) -> BehavioralFeatures:
        """Return minimal feature set when insufficient data"""
        return BehavioralFeatures(conversation_id=conversation_id)

    def _calculate_contact_frequency(self, messages: List[Message]) -> float:
        """
        Calculate escalation in contact frequency over time

        Method:
        - Divide timeline into segments
        - Compare message density across segments
        - Higher density in later segments indicates escalation

        Returns:
            Score from 0.0 to 1.0
        """
        if len(messages) < 3:
            return 0.0

        # Get adult messages only
        adult_messages = [m for m in messages if m.sender_role == SenderRole.ADULT]
        if len(adult_messages) < 3:
            return 0.0

        # Sort by timestamp
        adult_messages = sorted(adult_messages, key=lambda m: m.timestamp)

        # Divide into first half and second half
        midpoint = len(adult_messages) // 2
        first_half = adult_messages[:midpoint]
        second_half = adult_messages[midpoint:]

        # Calculate time spans
        first_duration = (first_half[-1].timestamp - first_half[0].timestamp).total_seconds() / 3600.0
        second_duration = (second_half[-1].timestamp - second_half[0].timestamp).total_seconds() / 3600.0

        # Avoid division by zero
        if first_duration < 0.1 or second_duration < 0.1:
            return 0.0

        # Calculate message density (messages per hour)
        first_density = len(first_half) / max(first_duration, 0.1)
        second_density = len(second_half) / max(second_duration, 0.1)

        # Calculate escalation ratio
        if first_density < 0.01:
            escalation = 1.0 if second_density > 0.1 else 0.0
        else:
            escalation = min(second_density / first_density, 3.0) / 3.0

        return float(np.clip(escalation, 0.0, 1.0))

    def _calculate_persistence(self, messages: List[Message]) -> float:
        """
        Calculate persistence after non-response

        Method:
        - Identify sequences where adult messages without minor responses
        - Measure length and frequency of such sequences

        Returns:
            Score from 0.0 to 1.0
        """
        if len(messages) < 3:
            return 0.0

        # Sort messages by timestamp
        sorted_messages = sorted(messages, key=lambda m: m.timestamp)

        consecutive_adult_sequences = []
        current_sequence = 0

        for msg in sorted_messages:
            if msg.sender_role == SenderRole.ADULT:
                current_sequence += 1
            elif msg.sender_role == SenderRole.MINOR:
                if current_sequence > 0:
                    consecutive_adult_sequences.append(current_sequence)
                current_sequence = 0

        # Add final sequence if exists
        if current_sequence > 0:
            consecutive_adult_sequences.append(current_sequence)

        if not consecutive_adult_sequences:
            return 0.0

        # Calculate persistence metrics
        max_sequence = max(consecutive_adult_sequences)
        avg_sequence = np.mean(consecutive_adult_sequences)

        # Normalize (sequences of 5+ messages indicate high persistence)
        persistence_score = min((max_sequence * 0.5 + avg_sequence * 0.5) / 5.0, 1.0)

        return float(np.clip(persistence_score, 0.0, 1.0))

    def _calculate_time_irregularity(self, messages: List[Message]) -> float:
        """
        Calculate messaging at unusual hours

        Method:
        - Identify messages outside normal hours (9 AM - 9 PM)
        - Weight by severity (late night hours more concerning)

        Returns:
            Score from 0.0 to 1.0
        """
        if not messages:
            return 0.0

        adult_messages = [m for m in messages if m.sender_role == SenderRole.ADULT]
        if not adult_messages:
            return 0.0

        irregular_count = 0
        highly_irregular_count = 0

        for msg in adult_messages:
            hour = msg.timestamp.hour

            # Late night / early morning (11 PM - 6 AM) - highly irregular
            if hour >= 23 or hour < 6:
                highly_irregular_count += 1
                irregular_count += 1
            # Outside normal hours but not extreme
            elif hour < self.normal_hour_start or hour >= self.normal_hour_end:
                irregular_count += 1

        # Calculate proportion of irregular messages
        irregular_ratio = irregular_count / len(adult_messages)
        highly_irregular_ratio = highly_irregular_count / len(adult_messages)

        # Weighted score (highly irregular hours weighted more)
        score = (irregular_ratio * 0.5 + highly_irregular_ratio * 0.5)

        return float(np.clip(score, 0.0, 1.0))

    def _calculate_emotional_dependency(self, messages: List[Message]) -> float:
        """
        Calculate emotional dependency indicators

        Method:
        - Analyze abstracted text for dependency patterns
        - Look for keywords suggesting emotional manipulation
        - Non-explicit, behavioral focus only
        - Multilingual support (English, Portuguese, Spanish)

        Returns:
            Score from 0.0 to 1.0
        """
        # Dependency indicator keywords (abstract, non-explicit) - Multilingual
        dependency_keywords = [
            # English
            'special', 'unique', 'understand', 'only one', 'secret',
            'nobody else', 'trust me', 'always there', 'need you',
            'miss you', 'thinking about', 'closest friend', 'special bond',
            # Portuguese
            'especial', 'único', 'única', 'entende', 'entender', 'compreende',
            'ninguém mais', 'só você', 'confie em mim', 'sempre aqui',
            'preciso de você', 'sinto sua falta', 'pensando em você',
            'melhor amigo', 'amigo especial', 'ninguém liga', 'ninguém entende',
            'você é diferente', 'te entendo', 'te compreendo', 'pode me chamar',
            # Spanish
            'especial', 'único', 'única', 'entiende', 'entender', 'comprende',
            'nadie más', 'solo tú', 'confía en mí', 'siempre aquí',
            'te necesito', 'te extraño', 'pensando en ti', 'mejor amigo'
        ]

        adult_messages = [m for m in messages if m.sender_role == SenderRole.ADULT]
        if not adult_messages:
            return 0.0

        keyword_matches = 0
        total_messages = len(adult_messages)

        for msg in adult_messages:
            text_lower = msg.abstracted_text.lower()
            for keyword in dependency_keywords:
                if keyword in text_lower:
                    keyword_matches += 1
                    break  # Count once per message

        # Normalize by message count
        dependency_score = min(keyword_matches / max(total_messages * 0.3, 1.0), 1.0)

        return float(np.clip(dependency_score, 0.0, 1.0))

    def _calculate_isolation_pressure(self, messages: List[Message]) -> float:
        """
        Calculate isolation pressure indicators

        Method:
        - Look for patterns suggesting attempts to isolate target
        - Keywords about meeting alone, keeping away from others
        - Multilingual support (English, Portuguese, Spanish)

        Returns:
            Score from 0.0 to 1.0
        """
        isolation_keywords = [
            # English
            'just us', 'alone', 'private', 'don\'t tell', 'keep between us',
            'our secret', 'without them', 'by ourselves', 'meet up',
            'come over', 'your parents', 'they don\'t understand',
            # Portuguese
            'só nós', 'sozinho', 'sozinha', 'sozinhos', 'privado', 'privada',
            'não contar', 'não conte', 'não contem', 'entre nós', 'só entre nós',
            'nosso segredo', 'sem eles', 'sem elas', 'vir aqui', 'vem aqui',
            'seus pais', 'sua família', 'não entendem', 'não vão entender',
            'exagerar', 'estragar', 'arruinar', 'ninguém precisa saber',
            # Spanish
            'solo nosotros', 'solos', 'privado', 'no digas', 'no cuentes',
            'entre nosotros', 'nuestro secreto', 'sin ellos', 'ven aquí',
            'tus padres', 'tu familia', 'no entienden', 'no van a entender'
        ]

        adult_messages = [m for m in messages if m.sender_role == SenderRole.ADULT]
        if not adult_messages:
            return 0.0

        keyword_matches = 0
        total_messages = len(adult_messages)

        for msg in adult_messages:
            text_lower = msg.abstracted_text.lower()
            for keyword in isolation_keywords:
                if keyword in text_lower:
                    keyword_matches += 1
                    break

        isolation_score = min(keyword_matches / max(total_messages * 0.2, 1.0), 1.0)

        return float(np.clip(isolation_score, 0.0, 1.0))

    def _calculate_secrecy_pressure(self, messages: List[Message]) -> float:
        """
        Calculate secrecy pressure indicators

        Method:
        - Identify requests for keeping communication secret
        - Pattern of emphasizing privacy or confidentiality
        - Multilingual support (English, Portuguese, Spanish)

        Returns:
            Score from 0.0 to 1.0
        """
        secrecy_keywords = [
            # English
            'secret', 'don\'t tell', 'keep this private', 'between us',
            'our little', 'confidential', 'nobody knows', 'hide',
            'delete', 'erase', 'password', 'private chat',
            # Portuguese
            'segredo', 'não contar', 'não conte', 'mantenha privado', 'manter privado',
            'entre nós', 'nosso', 'confidencial', 'ninguém sabe', 'esconder',
            'deletar', 'apagar', 'excluir', 'senha', 'conversa privada',
            'só nosso', 'só nossa', 'não diga', 'fica entre nós',
            # Spanish
            'secreto', 'no digas', 'no cuentes', 'mantener privado', 'entre nosotros',
            'nuestro', 'confidencial', 'nadie sabe', 'esconder', 'ocultar',
            'borrar', 'eliminar', 'contraseña', 'chat privado'
        ]

        adult_messages = [m for m in messages if m.sender_role == SenderRole.ADULT]
        if not adult_messages:
            return 0.0

        keyword_matches = 0
        total_messages = len(adult_messages)

        for msg in adult_messages:
            text_lower = msg.abstracted_text.lower()
            for keyword in secrecy_keywords:
                if keyword in text_lower:
                    keyword_matches += 1
                    break

        secrecy_score = min(keyword_matches / max(total_messages * 0.15, 1.0), 1.0)

        return float(np.clip(secrecy_score, 0.0, 1.0))

    def _calculate_platform_migration(self, messages: List[Message]) -> float:
        """
        Calculate platform migration attempts

        Method:
        - Look for mentions of other platforms or communication channels
        - Attempts to move conversation elsewhere
        - Multilingual support (English, Portuguese, Spanish)

        Returns:
            Score from 0.0 to 1.0
        """
        migration_keywords = [
            # English
            'snapchat', 'whatsapp', 'telegram', 'discord', 'instagram',
            'phone number', 'text me', 'dm me', 'add me on', 'private message',
            'different app', 'other platform', 'email me',
            # Portuguese
            'número de telefone', 'me manda mensagem', 'me chama', 'me adiciona',
            'mensagem privada', 'outro app', 'outro aplicativo', 'outra plataforma',
            'me manda email', 'passa seu número', 'qual seu número',
            # Spanish
            'número de teléfono', 'envíame mensaje', 'mándame mensaje', 'agrégame',
            'mensaje privado', 'otra aplicación', 'otra plataforma', 'envíame email',
            'pásame tu número'
        ]

        adult_messages = [m for m in messages if m.sender_role == SenderRole.ADULT]
        if not adult_messages:
            return 0.0

        keyword_matches = 0
        total_messages = len(adult_messages)

        for msg in adult_messages:
            text_lower = msg.abstracted_text.lower()
            for keyword in migration_keywords:
                if keyword in text_lower:
                    keyword_matches += 1
                    break

        migration_score = min(keyword_matches / max(total_messages * 0.15, 1.0), 1.0)

        return float(np.clip(migration_score, 0.0, 1.0))

    def _calculate_tone_shift(self, messages: List[Message]) -> float:
        """
        Calculate linguistic tone shift over time

        Method:
        - Analyze message length changes
        - Track formality/informality shifts
        - Measure sentiment progression (simple proxy)

        Returns:
            Score from 0.0 to 1.0
        """
        adult_messages = [m for m in messages if m.sender_role == SenderRole.ADULT]
        if len(adult_messages) < 4:
            return 0.0

        # Sort by timestamp
        adult_messages = sorted(adult_messages, key=lambda m: m.timestamp)

        # Divide into early and late periods
        midpoint = len(adult_messages) // 2
        early_messages = adult_messages[:midpoint]
        late_messages = adult_messages[midpoint:]

        # Calculate average message length in each period
        early_avg_length = np.mean([len(m.abstracted_text) for m in early_messages])
        late_avg_length = np.mean([len(m.abstracted_text) for m in late_messages])

        # Calculate length ratio (increasing length may indicate escalation)
        if early_avg_length > 0:
            length_shift = abs(late_avg_length - early_avg_length) / early_avg_length
        else:
            length_shift = 0.0

        # Normalize (50% change or more = max score)
        tone_shift_score = min(length_shift / 0.5, 1.0)

        return float(np.clip(tone_shift_score, 0.0, 1.0))
