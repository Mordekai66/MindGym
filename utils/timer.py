import pygame

class Timer:
    """A simple timer class for tracking game time"""
    
    def __init__(self, duration):
        """Initialize the timer with a duration in seconds"""
        self.duration = duration * 1000  # Convert to milliseconds
        self.start_time = pygame.time.get_ticks()
        self.paused = False
        self.pause_time = 0
        self.time_paused = 0
    
    def update(self):
        """Update the timer"""
        if not self.paused:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time - self.time_paused
            return elapsed < self.duration
        return True
    
    def get_time_left(self):
        """Get the time left in seconds"""
        if self.paused:
            elapsed = self.pause_time - self.start_time - self.time_paused
        else:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time - self.time_paused
        
        time_left = max(0, self.duration - elapsed)
        return time_left / 1000  # Convert to seconds
    
    def is_expired(self):
        """Check if the timer has expired"""
        return self.get_time_left() <= 0
    
    def pause(self):
        """Pause the timer"""
        if not self.paused:
            self.paused = True
            self.pause_time = pygame.time.get_ticks()
    
    def resume(self):
        """Resume the timer"""
        if self.paused:
            self.time_paused += pygame.time.get_ticks() - self.pause_time
            self.paused = False