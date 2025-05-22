import pygame

from entities.Object import map1
from engine.database import add_score

GRAVITY = 1
FRICTION = 0.90

DEAD_SPEED = 28


def detectCollison(self):
    if self.isTakingDamage:
        return
    
    screen_width = pygame.display.get_surface().get_width()
    screen_height = pygame.display.get_surface().get_height()

    if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height :
        self.isTakingDamage = True
        self.handleDamage()
        self.isTakingDamage = False
        return

    CollisionTestRect = self.rect.copy()
    CollisionTestRect.x += self.CurrentFrameDistance.x


    # check on x axis
    for obj in map1.objects:
        if CollisionTestRect.colliderect(obj.object):
            # if force was to high then explode
            if self.currentSpeed.x > DEAD_SPEED or self.currentSpeed.x < -DEAD_SPEED :
                self.isTakingDamage = True
                self.handleDamage()
                self.isTakingDamage = False
                return

            # reset test rect to check on y axis
            CollisionTestRect.x -= self.CurrentFrameDistance.x

            if self.CurrentFrameDistance.x > 0: 
                self.CurrentFrameDistance.x = obj.object.left - self.rect.right
            else:
                self.CurrentFrameDistance.x = obj.object.right - self.rect.left
    
    # check on y axis
    CollisionTestRect.y += self.CurrentFrameDistance.y

    for obj in map1.objects:
        if CollisionTestRect.colliderect(obj.object):
            # if colision when going down then on ground
            if self.CurrentFrameDistance.y > 0:
                self.isGrounded = True
                self.CurrentFrameDistance.y = obj.object.top - self.rect.bottom
            else:
                self.CurrentFrameDistance.y = obj.object.bottom - self.rect.top
                self.currentSpeed.y = 0


def bulletCollision(self, players):
    for player in players:
        if self.rect.colliderect(player.rect) and self.shooter != player.PlayerID:
                self.kill()
                player.hp -= 1
                if player.hp == 0:
                    player.isTakingDamage = True
                    player.handleDamage()
                    player.isTakingDamage = False


                break
def applyGravity(self):
    if self.isTakingDamage:
        return
        
    self.currentSpeed.y += GRAVITY
    detectCollison(self)

def applyFriction(self):
    if self.isTakingDamage:
        return
        
    # stop if to slow
    if abs(self.currentSpeed.x) < 0.1:
        self.currentSpeed.x = 0
        return
    
    self.currentSpeed.x *= FRICTION

    # max speed handle
    if abs(self.currentSpeed.x) > self.max_x_velocity:
        self.currentSpeed.x = self.max_x_velocity * (1 if self.currentSpeed.x > 0 else -1)

#fonction that check collisons between players
def checkPlayerCollision(Players):
    for i, player in enumerate(Players):
        for j, other_player in enumerate(Players):
            # don't check himself
            if i != j:
                #check for colision
                if player.rect.colliderect(other_player.rect) and not player.wasBumped and not player.isDead:  
                    #check if the player should push of be pushed
                    if abs(player.currentSpeed.x) > abs(other_player.currentSpeed.x):
                        if player.rect.x < other_player.rect.x:
                            other_player.currentSpeed.x += abs(player.currentSpeed.x) * player.bumpPower
                        else:
                            other_player.currentSpeed.x -= abs(player.currentSpeed.x) * player.bumpPower
                            
                        #push player up 
                        other_player.currentSpeed.y -= player.bumpPower
                        other_player.isGrounded = False
                        other_player.wasBumped = True


def checkEndGame(players):
    alivePlayersCount = 0
    for player in players:
        if not player.isDead:
            alivePlayersCount += 1
            if alivePlayersCount > 1:
                return False
    return True


'''
def saveScore(winner):        
    file_path = os.path.join("database", "data.json")
    
    try:
        # load json
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # increase winner score
        winner_id = str(winner.PlayerID)
        if winner_id not in data["scores"]:
            data["scores"][winner_id] = 0
        data["scores"][winner_id] += 1
        
        # save json
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        
            
    except Exception as e:
        print(f"Error while saving score: {e}")
'''

def saveScore(winner, playersCount):
    score = winner.health * playersCount * 100
    add_score(winner.PlayerID+1, score)
    