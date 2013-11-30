import random
random.seed()
class Personality(object):
    #Passing around classes instead of strings or something, sort of like an enum.
    class Affectionate(object):
        stat = 'hpm'
    
    class Aggressive(object):
        stat = 'atk'
    
    class Careful(object):
        stat = 'def'
    
    class Energetic(object):
        stat = 'spd'
    
    @classmethod
    def random(cls):
        """Return a random personality."""
        return random.choice((cls.Affectionate, cls.Aggressive, cls.Careful, cls.Energetic))
        
    @classmethod
    def generateName(cls, mon_personality):
        """Generate a name for a monster."""
        #fill in with unique syllables
        if mon_personality in (cls.Affectionate, cls.Careful):
            temp_name = random.choice(("fa","ji","sy","ba","vi","pho")) + random.choice(("la","lo","mog","ta"))
        else:#cls.Aggressive, cls.Energetic
            temp_name = random.choice(("ga","ku","zi","ru","te","the")) + random.choice(("va","iy","na","ran"))
        return temp_name + random.choice(("ex","ul","av","em","ix","ab","ev","og","za","el"))
        
class Mood(object):
    #So instead of using numbers/strings/whatever for moods, just use Mood.the_mood
    #This way, if something is mistyped or whatever we will get an error, useful.
    neutral = 0
    bored   = 1
    sad     = 2
    angry   = 3
    happy   = 4
    