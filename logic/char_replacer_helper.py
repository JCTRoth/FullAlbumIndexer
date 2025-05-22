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
        text = text.replace("̤", "")
        text = text.replace("̲", "")
        text = text.replace("_", "")
        text = text.replace("∙", "")
        
        # Replace special characters with their normal equivalents
        # Uppercase
        text = text.replace("Ḧ", "H")
        text = text.replace("Ṳ", "U")
        text = text.replace("Ẍ", "X")
        text = text.replace("Ạ", "A")
        text = text.replace("Ḅ", "B")
        text = text.replace("Ḍ", "D")
        text = text.replace("Ḥ", "H")
        text = text.replace("Ị", "I")
        text = text.replace("Ḳ", "K")
        text = text.replace("Ḷ", "L")
        text = text.replace("Ṃ", "M")
        text = text.replace("Ṇ", "N")
        text = text.replace("Ṛ", "R")
        text = text.replace("Ṣ", "S")
        text = text.replace("Ṭ", "T")
        text = text.replace("Ụ", "U")
        text = text.replace("Ṿ", "V")
        text = text.replace("Ẉ", "W")
        text = text.replace("Ỵ", "Y")
        text = text.replace("Ẓ", "Z")
        
        # Lowercase
        text = text.replace("ḧ", "h")
        text = text.replace("ṳ", "u")
        text = text.replace("ẍ", "x")
        text = text.replace("ạ", "a")
        text = text.replace("ḅ", "b")
        text = text.replace("ḍ", "d")
        text = text.replace("ḥ", "h")
        text = text.replace("ị", "i")
        text = text.replace("ḳ", "k")
        text = text.replace("ḷ", "l")
        text = text.replace("ṃ", "m")
        text = text.replace("ṇ", "n")
        text = text.replace("ṛ", "r")
        text = text.replace("ṣ", "s")
        text = text.replace("ṭ", "t")
        text = text.replace("ụ", "u")
        text = text.replace("ṿ", "v")
        text = text.replace("ẉ", "w")
        text = text.replace("ỵ", "y")
        text = text.replace("ẓ", "z")
        
        return text 