// GROOMSAFE Internationalization (i18n)
// Supports: English, Portuguese, Spanish

const translations = {
    en: {
        // Header
        title: "GROOMSAFE",
        subtitle: "Behavioral Risk Assessment Platform",
        apiStatus: "API Status",

        // Quick Load Examples
        quickLoad: "Quick Load Example",
        lowRisk: "Low Risk",
        moderateRisk: "Moderate Risk",
        highRisk: "High Risk",
        criticalRisk: "Critical Risk",
        educationalConversation: "Educational Conversation",
        concerningPatterns: "Concerning Patterns",
        multipleIndicators: "Multiple Indicators",
        escalationDetected: "Escalation Detected",

        // Form
        conversationAnalysis: "Conversation Analysis",
        manualInput: "Manual Input",
        platformType: "Platform Type",
        socialMedia: "Social Media",
        messagingApp: "Messaging App",
        gamingPlatform: "Gaming Platform",
        educationalForum: "Educational Forum",
        other: "Other",
        addMessages: "Add Messages (JSON format or use message builder below)",
        messageBuilder: "Message Builder",
        adult: "Adult",
        minor: "Minor",
        messageText: "Message text...",
        addMessage: "Add Message",
        analystExposureLevel: "Analyst Exposure Level",
        minimal: "Minimal (Default)",
        moderate: "Moderate",
        detailed: "Detailed",
        analystId: "Analyst ID (Optional)",
        analyzeConversation: "Analyze Conversation",

        // LLM Section
        llmEnhanced: "LLM-Enhanced Analysis (Optional)",
        enableLLM: "Enable LLM Analysis",
        llmDescription: "Uses AI to enrich behavioral detection",
        provider: "Provider",
        ollamaLocal: "Ollama (Local, Free)",
        gemini: "Google Gemini",
        claude: "Anthropic Claude",
        chatgpt: "OpenAI ChatGPT",
        model: "Model",
        apiKey: "API Key",
        apiKeyRequired: "Required for cloud providers",
        testConnection: "Test Connection",

        // Results
        analysisResults: "Analysis Results",
        noAnalysisYet: "No analysis yet. Load an example or submit a conversation to begin.",
        analyzingPatterns: "Analyzing conversation patterns...",
        riskAssessment: "Risk Assessment",
        confidence: "Confidence",
        stage: "Stage",
        humanReview: "Human Review",
        required: "Required",
        notRequired: "Not Required",

        // Behavioral Features
        behavioralFeatures: "Behavioral Features",
        contactFrequency: "Contact Frequency",
        persistence: "Persistence After Non-Response",
        timeIrregularity: "Time of Day Irregularity",
        emotionalDependency: "Emotional Dependency",
        isolationPressure: "Isolation Pressure",
        secrecyPressure: "Secrecy Pressure",
        platformMigration: "Platform Migration",
        toneShift: "Tone Shift",

        // LLM Analysis
        aiEnhancedAnalysis: "AI-Enhanced Analysis",
        aiSeverity: "AI Severity Assessment",
        analysisExplanation: "Analysis Explanation",
        groomingIndicators: "Grooming Indicators Detected",
        riskFactors: "Risk Factors",

        // HUMANSHIELD
        humanshieldSummary: "HUMANSHIELD Protection Summary",
        behavioralCluster: "Behavioral Cluster",
        temporalPattern: "Temporal Pattern",
        keyRiskIndicators: "Key Risk Indicators",

        // Recommendations
        recommendedActions: "Recommended Actions",
        topContributing: "Top Contributing Features",

        // Export
        exportReport: "Export Report",
        exportJSON: "Export JSON",
        exportPDF: "Export PDF",

        // Language
        language: "Language",

        // Footer
        footerText: "Behavioral Grooming Prevention & Investigator Protection Platform",
        apiDocs: "API Docs",
        documentation: "Documentation",

        // Stages
        initialContact: "Initial Contact",
        trustBuilding: "Trust Building",
        emotionalDependencyStage: "Emotional Dependency",
        isolationAttempts: "Isolation Attempts",
        escalationRisk: "Escalation Risk",
        unknown: "Unknown"
    },

    pt: {
        // Header
        title: "GROOMSAFE",
        subtitle: "Plataforma de Avaliação de Risco Comportamental",
        apiStatus: "Status da API",

        // Quick Load Examples
        quickLoad: "Carregar Exemplo Rápido",
        lowRisk: "Risco Baixo",
        moderateRisk: "Risco Moderado",
        highRisk: "Risco Alto",
        criticalRisk: "Risco Crítico",
        educationalConversation: "Conversa Educacional",
        concerningPatterns: "Padrões Preocupantes",
        multipleIndicators: "Múltiplos Indicadores",
        escalationDetected: "Escalação Detectada",

        // Form
        conversationAnalysis: "Análise de Conversa",
        manualInput: "Entrada Manual",
        platformType: "Tipo de Plataforma",
        socialMedia: "Redes Sociais",
        messagingApp: "App de Mensagens",
        gamingPlatform: "Plataforma de Jogos",
        educationalForum: "Fórum Educacional",
        other: "Outro",
        addMessages: "Adicionar Mensagens (formato JSON ou use o construtor abaixo)",
        messageBuilder: "Construtor de Mensagens",
        adult: "Adulto",
        minor: "Menor",
        messageText: "Texto da mensagem...",
        addMessage: "Adicionar Mensagem",
        analystExposureLevel: "Nível de Exposição do Analista",
        minimal: "Mínimo (Padrão)",
        moderate: "Moderado",
        detailed: "Detalhado",
        analystId: "ID do Analista (Opcional)",
        analyzeConversation: "Analisar Conversa",

        // LLM Section
        llmEnhanced: "Análise Aprimorada por IA (Opcional)",
        enableLLM: "Ativar Análise por IA",
        llmDescription: "Usa IA para enriquecer a detecção comportamental",
        provider: "Provedor",
        ollamaLocal: "Ollama (Local, Gratuito)",
        gemini: "Google Gemini",
        claude: "Anthropic Claude",
        chatgpt: "OpenAI ChatGPT",
        model: "Modelo",
        apiKey: "Chave API",
        apiKeyRequired: "Obrigatório para provedores em nuvem",
        testConnection: "Testar Conexão",

        // Results
        analysisResults: "Resultados da Análise",
        noAnalysisYet: "Nenhuma análise ainda. Carregue um exemplo ou envie uma conversa para começar.",
        analyzingPatterns: "Analisando padrões de conversa...",
        riskAssessment: "Avaliação de Risco",
        confidence: "Confiança",
        stage: "Estágio",
        humanReview: "Revisão Humana",
        required: "Necessária",
        notRequired: "Não Necessária",

        // Behavioral Features
        behavioralFeatures: "Características Comportamentais",
        contactFrequency: "Frequência de Contato",
        persistence: "Persistência Após Não-Resposta",
        timeIrregularity: "Irregularidade de Horário",
        emotionalDependency: "Dependência Emocional",
        isolationPressure: "Pressão de Isolamento",
        secrecyPressure: "Pressão de Sigilo",
        platformMigration: "Migração de Plataforma",
        toneShift: "Mudança de Tom",

        // LLM Analysis
        aiEnhancedAnalysis: "Análise Aprimorada por IA",
        aiSeverity: "Avaliação de Severidade da IA",
        analysisExplanation: "Explicação da Análise",
        groomingIndicators: "Indicadores de Aliciamento Detectados",
        riskFactors: "Fatores de Risco",

        // HUMANSHIELD
        humanshieldSummary: "Resumo de Proteção HUMANSHIELD",
        behavioralCluster: "Cluster Comportamental",
        temporalPattern: "Padrão Temporal",
        keyRiskIndicators: "Principais Indicadores de Risco",

        // Recommendations
        recommendedActions: "Ações Recomendadas",
        topContributing: "Principais Características Contribuintes",

        // Export
        exportReport: "Exportar Relatório",
        exportJSON: "Exportar JSON",
        exportPDF: "Exportar PDF",

        // Language
        language: "Idioma",

        // Footer
        footerText: "Plataforma de Prevenção de Aliciamento & Proteção de Investigadores",
        apiDocs: "Documentação da API",
        documentation: "Documentação",

        // Stages
        initialContact: "Contato Inicial",
        trustBuilding: "Construção de Confiança",
        emotionalDependencyStage: "Dependência Emocional",
        isolationAttempts: "Tentativas de Isolamento",
        escalationRisk: "Risco de Escalação",
        unknown: "Desconhecido"
    },

    es: {
        // Header
        title: "GROOMSAFE",
        subtitle: "Plataforma de Evaluación de Riesgo Conductual",
        apiStatus: "Estado de la API",

        // Quick Load Examples
        quickLoad: "Cargar Ejemplo Rápido",
        lowRisk: "Riesgo Bajo",
        moderateRisk: "Riesgo Moderado",
        highRisk: "Riesgo Alto",
        criticalRisk: "Riesgo Crítico",
        educationalConversation: "Conversación Educativa",
        concerningPatterns: "Patrones Preocupantes",
        multipleIndicators: "Múltiples Indicadores",
        escalationDetected: "Escalada Detectada",

        // Form
        conversationAnalysis: "Análisis de Conversación",
        manualInput: "Entrada Manual",
        platformType: "Tipo de Plataforma",
        socialMedia: "Redes Sociales",
        messagingApp: "App de Mensajería",
        gamingPlatform: "Plataforma de Juegos",
        educationalForum: "Foro Educativo",
        other: "Otro",
        addMessages: "Agregar Mensajes (formato JSON o usar constructor)",
        messageBuilder: "Constructor de Mensajes",
        adult: "Adulto",
        minor: "Menor",
        messageText: "Texto del mensaje...",
        addMessage: "Agregar Mensaje",
        analystExposureLevel: "Nivel de Exposición del Analista",
        minimal: "Mínimo (Predeterminado)",
        moderate: "Moderado",
        detailed: "Detallado",
        analystId: "ID del Analista (Opcional)",
        analyzeConversation: "Analizar Conversación",

        // LLM Section
        llmEnhanced: "Análisis Mejorado por IA (Opcional)",
        enableLLM: "Activar Análisis por IA",
        llmDescription: "Usa IA para enriquecer la detección conductual",
        provider: "Proveedor",
        ollamaLocal: "Ollama (Local, Gratis)",
        gemini: "Google Gemini",
        claude: "Anthropic Claude",
        chatgpt: "OpenAI ChatGPT",
        model: "Modelo",
        apiKey: "Clave API",
        apiKeyRequired: "Requerido para proveedores en la nube",
        testConnection: "Probar Conexión",

        // Results
        analysisResults: "Resultados del Análisis",
        noAnalysisYet: "Sin análisis aún. Cargue un ejemplo o envíe una conversación para comenzar.",
        analyzingPatterns: "Analizando patrones de conversación...",
        riskAssessment: "Evaluación de Riesgo",
        confidence: "Confianza",
        stage: "Etapa",
        humanReview: "Revisión Humana",
        required: "Requerida",
        notRequired: "No Requerida",

        // Behavioral Features
        behavioralFeatures: "Características Conductuales",
        contactFrequency: "Frecuencia de Contacto",
        persistence: "Persistencia Después de No Respuesta",
        timeIrregularity: "Irregularidad de Horario",
        emotionalDependency: "Dependencia Emocional",
        isolationPressure: "Presión de Aislamiento",
        secrecyPressure: "Presión de Secreto",
        platformMigration: "Migración de Plataforma",
        toneShift: "Cambio de Tono",

        // LLM Analysis
        aiEnhancedAnalysis: "Análisis Mejorado por IA",
        aiSeverity: "Evaluación de Severidad de IA",
        analysisExplanation: "Explicación del Análisis",
        groomingIndicators: "Indicadores de Acoso Detectados",
        riskFactors: "Factores de Riesgo",

        // HUMANSHIELD
        humanshieldSummary: "Resumen de Protección HUMANSHIELD",
        behavioralCluster: "Grupo Conductual",
        temporalPattern: "Patrón Temporal",
        keyRiskIndicators: "Indicadores Clave de Riesgo",

        // Recommendations
        recommendedActions: "Acciones Recomendadas",
        topContributing: "Principales Características Contribuyentes",

        // Export
        exportReport: "Exportar Informe",
        exportJSON: "Exportar JSON",
        exportPDF: "Exportar PDF",

        // Language
        language: "Idioma",

        // Footer
        footerText: "Plataforma de Prevención de Acoso & Protección de Investigadores",
        apiDocs: "Documentación de API",
        documentation: "Documentación",

        // Stages
        initialContact: "Contacto Inicial",
        trustBuilding: "Construcción de Confianza",
        emotionalDependencyStage: "Dependencia Emocional",
        isolationAttempts: "Intentos de Aislamiento",
        escalationRisk: "Riesgo de Escalada",
        unknown: "Desconocido"
    }
};

// Current language state
let currentLanguage = 'en';

// Get translation
function t(key) {
    return translations[currentLanguage][key] || key;
}

// Set language
function setLanguage(lang) {
    if (!translations[lang]) {
        console.error(`Language ${lang} not supported`);
        return;
    }

    currentLanguage = lang;
    localStorage.setItem('groomsafe_language', lang);
    updateUI();
}

// Update UI with current language
function updateUI() {
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translation = t(key);

        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = translation;
        } else {
            el.textContent = translation;
        }
    });
}

// Initialize language on page load
function initI18n() {
    // Load saved language or default to English
    const savedLang = localStorage.getItem('groomsafe_language') || 'en';
    setLanguage(savedLang);
}

// Export functions
window.t = t;
window.setLanguage = setLanguage;
window.initI18n = initI18n;
