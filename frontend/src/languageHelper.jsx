// Language helper object for field labels
const lang_helper = {
  en: {
    // Basic herb information
    name: "Name",
    scientific_name: "Scientific Name",
    common_names: "Common Names",
    ayush_system: "AYUSH System",
    parts_used: "Parts Used",
    uses: "Uses",
    properties: "Properties",
    contraindications: "Contraindications",
    precautions: "Precautions",
    
    // Remedy information
    remedies: "Remedies",
    condition: "Condition",
    preparation: "Preparation",
    dosage: "Dosage",
    
    // UI labels
    detailed_information: "Detailed Information",
    traditional_preparations: "Traditional Preparations",
    related_conditions: "Related Conditions",
    safety_information: "Safety Information",
    
    // Status messages
    loading: "Loading...",
    no_data: "No data available",
    search_placeholder: "Ask about herbs or health concerns...",
    
    // Actions
    search: "Search",
    clear: "Clear",
    back: "Back",
    more_info: "More Information"
  },
  
  hi: {
    // Basic herb information
    name: "नाम",
    scientific_name: "वैज्ञानिक नाम",
    common_names: "सामान्य नाम",
    ayush_system: "आयुष पद्धति",
    parts_used: "उपयोगी भाग",
    uses: "उपयोग",
    properties: "गुण",
    contraindications: "मतभेद",
    precautions: "सावधानियां",
    
    // Remedy information
    remedies: "उपचार",
    condition: "स्थिति",
    preparation: "तैयारी",
    dosage: "मात्रा",
    
    // UI labels
    detailed_information: "विस्तृत जानकारी",
    traditional_preparations: "पारंपरिक तैयारी",
    related_conditions: "संबंधित रोग",
    safety_information: "सुरक्षा जानकारी",
    
    // Status messages
    loading: "लोड हो रहा है...",
    no_data: "कोई डेटा उपलब्ध नहीं",
    search_placeholder: "जड़ी-बूटियों या स्वास्थ्य चिंताओं के बारे में पूछें...",
    
    // Actions
    search: "खोजें",
    clear: "साफ़ करें",
    back: "वापस",
    more_info: "अधिक जानकारी"
  },
  
  mr: {
    // Basic herb information
    name: "नाव",
    scientific_name: "वैज्ञानिक नाव",
    common_names: "सामान्य नावे",
    ayush_system: "आयुष पद्धती",
    parts_used: "वापरण्याचे भाग",
    uses: "उपयोग",
    properties: "गुणधर्म",
    contraindications: "विरोधाभास",
    precautions: "खबरदारी",
    
    // Remedy information
    remedies: "उपचार",
    condition: "स्थिती",
    preparation: "तयारी",
    dosage: "डोस",
    
    // UI labels
    detailed_information: "तपशीलवार माहिती",
    traditional_preparations: "पारंपरिक तयारी",
    related_conditions: "संबंधित आजार",
    safety_information: "सुरक्षा माहिती",
    
    // Status messages
    loading: "लोड होत आहे...",
    no_data: "डेटा उपलब्ध नाही",
    search_placeholder: "औषधी वनस्पती किंवा आरोग्य समस्यांबद्दल विचारा...",
    
    // Actions
    search: "शोधा",
    clear: "साफ करा",
    back: "परत",
    more_info: "अधिक माहिती"
  }
};

// Helper function to get label in specific language
const getLabel = (language, key) => {
  return lang_helper[language]?.[key] || lang_helper['en'][key] || key;
};

// Helper function to get all labels for a language
const getLabelsForLanguage = (language) => {
  return lang_helper[language] || lang_helper['en'];
};

// Example usage in your React component:
const ExampleUsage = ({ herbData, language }) => {
  return (
    <div>
      <h3>{getLabel(language, 'name')}: {herbData.name}</h3>
      <p>{getLabel(language, 'scientific_name')}: {herbData.scientific_name}</p>
      <p>{getLabel(language, 'parts_used')}: {herbData.parts_used}</p>
      <p>{getLabel(language, 'uses')}: {herbData.uses}</p>
      
      {herbData.remedies && herbData.remedies.length > 0 && (
        <div>
          <h4>{getLabel(language, 'remedies')}:</h4>
          {herbData.remedies.map((remedy, index) => (
            <div key={index}>
              <strong>{getLabel(language, 'condition')}:</strong> {remedy.condition}<br/>
              <strong>{getLabel(language, 'preparation')}:</strong> {remedy.preparation}<br/>
              {remedy.dosage && (
                <>
                  <strong>{getLabel(language, 'dosage')}:</strong> {remedy.dosage}
                </>
              )}
            </div>
          ))}
        </div>
      )}
      
      {herbData.contraindications && (
        <p>
          <strong>{getLabel(language, 'precautions')}:</strong> {herbData.contraindications}
        </p>
      )}
    </div>
  );
};

export { lang_helper, getLabel, getLabelsForLanguage };