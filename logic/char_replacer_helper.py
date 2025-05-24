import unicodedata

class TextCleaner:
    @staticmethod
    def clean_special_characters(text: str) -> str:
        """
        Clean special characters from text, replacing them with their standard equivalents.
        
        Args:
            text (str): The text to clean
            
        Returns:
            str: The cleaned text
        """
        # Basic cleanup
        text = text.replace("̤", "")  # U+0324 COMBINING DIAERESIS BELOW
        text = text.replace("̲", "")  # U+0332 COMBINING LOW LINE
        text = text.replace("͟", "")  # U+035F COMBINING DOUBLE MACRON BELOW
        text = text.replace("_", "")
        text = text.replace("∙", "")
        
        # Replace special characters with their normal equivalents
        # Uppercase
        # Remove any remaining combining characters
        text = ''.join(c for c in text if not unicodedata.combining(c))
        
        return text.strip() 