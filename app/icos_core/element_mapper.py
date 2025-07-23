"""
ICOS Search Engine - Dynamic Element Identifier Management

This module handles the mapping and transformation of search result elements
for consistent styling and processing across the ICOS search platform.
"""

from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import logging


class SearchElementMapper:
    """
    Advanced element classification system for ICOS search results.
    
    Manages dynamic CSS class transformations and element identification
    to ensure consistent rendering and styling across search result pages.
    """
    
    def __init__(self):
        """Initialize the ICOS element mapping configuration."""
        self._initialize_element_registry()
        self._setup_transformation_rules()
        
    def _initialize_element_registry(self) -> None:
        """Configure the core element identifiers used throughout ICOS."""
        # Primary navigation and interface elements
        self.primary_tab_identifier = 'KP7LCb'
        self.media_tab_identifier = 'n692Zd' 
        self.page_footer_element = 'TuS8Ad'
        self.horizontal_divider = 'BsXmcf'
        self.content_scroller = 'idg8be'
        
        # Search result container classifications
        self.primary_result_container = 'ZINbbc'
        self.secondary_result_container = 'luh4td'
        
    def _setup_transformation_rules(self) -> None:
        """Define the element transformation mapping rules."""
        self._transformation_registry = {
            self.primary_result_container: ['Gx5Zad'],
            self.secondary_result_container: ['fP1Qef']
        }
    
    @property
    def main_tbm_tab(self) -> str:
        """Access the main tab element identifier."""
        return self.primary_tab_identifier
        
    @property 
    def images_tbm_tab(self) -> str:
        """Access the images tab element identifier."""
        return self.media_tab_identifier
        
    @property
    def footer(self) -> str:
        """Access the footer element identifier."""
        return self.page_footer_element
        
    @property
    def result_class_a(self) -> str:
        """Access the primary result class identifier."""
        return self.primary_result_container
        
    @property
    def result_class_b(self) -> str:
        """Access the secondary result class identifier."""
        return self.secondary_result_container
        
    @property
    def scroller_class(self) -> str:
        """Access the scroller element identifier."""
        return self.content_scroller
        
    @property
    def line_tag(self) -> str:
        """Access the line divider element identifier."""
        return self.horizontal_divider
        
    @property
    def result_classes(self) -> Dict[str, List[str]]:
        """Access the complete transformation registry."""
        return self._transformation_registry

    def transform_page_elements(self, page_content: BeautifulSoup) -> BeautifulSoup:
        """
        Apply element transformations to ensure consistent ICOS styling.
        
        This method processes search result pages and applies necessary
        class transformations to maintain proper styling and functionality.
        
        Args:
            page_content: BeautifulSoup object containing the page to transform
            
        Returns:
            BeautifulSoup: The transformed page with updated element classes
        """
        try:
            # Locate all divs that need transformation
            target_elements = self._find_transformable_elements(page_content)
            
            # Apply transformations to each located element
            for element in target_elements:
                self._apply_element_transformation(element)
                
            return page_content
            
        except Exception as transform_error:
            logging.warning(f"Element transformation encountered issue: {transform_error}")
            return page_content
    
    def _find_transformable_elements(self, content: BeautifulSoup) -> List[Any]:
        """
        Identify all page elements that require class transformation.
        
        Args:
            content: The BeautifulSoup content to search
            
        Returns:
            List of elements that need transformation
        """
        # Build list of all classes that need to be found
        search_classes = []
        for class_list in self._transformation_registry.values():
            search_classes.extend(class_list)
            
        # Find all div elements with these classes
        return content.find_all('div', {'class': search_classes})
    
    def _apply_element_transformation(self, element: Any) -> None:
        """
        Transform a single element's class attributes.
        
        Args:
            element: The BeautifulSoup element to transform
        """
        if not element.get('class'):
            return
            
        current_classes = ' '.join(element['class'])
        transformed_classes = current_classes
        
        # Apply each transformation rule
        for target_class, source_classes in self._transformation_registry.items():
            for source_class in source_classes:
                transformed_classes = transformed_classes.replace(source_class, target_class)
        
        # Update the element with transformed classes
        element['class'] = transformed_classes.split(' ')


# Maintain compatibility with existing ICOS codebase
GClasses = SearchElementMapper()

# Legacy method alias for backward compatibility  
def replace_css_classes(soup: BeautifulSoup) -> BeautifulSoup:
    """Legacy compatibility function for CSS class replacement."""
    mapper = SearchElementMapper()
    return mapper.transform_page_elements(soup)

# Add the method to the instance for compatibility
GClasses.replace_css_classes = lambda soup: GClasses.transform_page_elements(soup)
