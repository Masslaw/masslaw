class InvalidNumberOfPrintTargetImages(ValueError):
    def __init__(self, target_number_of_images: int, provided_number_of_images: int):
        super().__init__(f'Expected {target_number_of_images} images, got {provided_number_of_images}')
