def garantir_iframe(self, iframe):
    """Garante que o script está no iframe correto.
    Args:
        sb: Instância do seleniumbase
        iframe: Elemento ou seletor do iframe
    """
    try:
        self.switch_to_default_content()
        self.wait_for_element_visible(iframe, timeout=30)
        if self.is_element_visible(iframe):
            self.switch_to_default_content()
            self.switch_to_frame(self.find_element(iframe))
        else:
            raise Exception(f"Frame '{iframe}' não está visível.")
    
    except Exception as e:
        print(f"Erro ao alternar para o frame '{iframe}': {e}")