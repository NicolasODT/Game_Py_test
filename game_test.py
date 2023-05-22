import pygame
import random
import math
import time

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
largeur_ecran = 800
hauteur_ecran = 600
vitesse_vaisseau = 5
vitesse_tir = 7
vitesse_ennemi = 2
nb_ennemis = 10

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

# Création de l'écran
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption('Shoot Them Up')

# Police de caractères pour le score et les vies
police = pygame.font.Font(None, 36)


class Vaisseau(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 30
        self.height = 30
        self.color = VERT
        self.rect = pygame.Rect(
            largeur_ecran / 2, hauteur_ecran / 2, self.width, self.height)
        self.clignotement = False
        self.clignotement_start = 0
        self.clignotement_timer = 0

    def clignoter(self):
        if self.clignotement:
            if time.time() - self.clignotement_timer > 0.1:
                self.color = NOIR if self.color == VERT else VERT
                self.clignotement_timer = time.time()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self, keys):
        self.clignoter()
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= vitesse_vaisseau
        if keys[pygame.K_DOWN] and self.rect.y < hauteur_ecran - self.rect.height:
            self.rect.y += vitesse_vaisseau
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= vitesse_vaisseau
        if keys[pygame.K_RIGHT] and self.rect.x < largeur_ecran - self.rect.width:
            self.rect.x += vitesse_vaisseau


class Tir(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.width = 10
        self.height = 10
        self.color = BLANC
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.dx = dx
        self.dy = dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        self.rect.x += self.dx * vitesse_tir
        self.rect.y += self.dy * vitesse_tir


class Ennemi(pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__()
        self.width = 30
        self.height = 30
        self.color = ROUGE
        self.spawn_side = random.choice(["top", "bottom", "left", "right"])
        if self.spawn_side == "top":
            self.rect = pygame.Rect(random.randint(0, largeur_ecran - self.width),
                                    random.randint(-hauteur_ecran, -self.height), self.width, self.height)
        elif self.spawn_side == "bottom":
            self.rect = pygame.Rect(random.randint(0, largeur_ecran - self.width),
                                    random.randint(hauteur_ecran, hauteur_ecran + self.height), self.width, self.height)
        elif self.spawn_side == "left":
            self.rect = pygame.Rect(random.randint(-largeur_ecran, -self.width),
                                    random.randint(0, hauteur_ecran - self.height), self.width, self.height)
        else:
            self.rect = pygame.Rect(random.randint(largeur_ecran, largeur_ecran + self.width),
                                    random.randint(0, hauteur_ecran - self.height), self.width, self.height)

        self.x_offset = random.randint(1, 3) * random.choice([-1, 1])
        self.target = target
        self.speed_factor = random.uniform(0.5, 1)
        # Ajustez les valeurs en fonction du nombre de vies souhaité
        self.vies = random.randint(1, 4)
        self.color = self.get_color_from_vies(self.vies)

    def get_color_from_vies(self, vies):
        return (255 - 50 * vies, 0, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        dx = self.target.rect.x - self.rect.x
        dy = self.target.rect.y - self.rect.y
        dist = math.sqrt(dx * dx + dy * dy)
        self.rect.x += (dx / dist) * vitesse_ennemi * self.speed_factor
        self.rect.y += (dy / dist) * vitesse_ennemi * self.speed_factor
        if self.spawn_side == "top" and self.rect.y > hauteur_ecran:
            self.rect.y = random.randint(-hauteur_ecran, -self.rect.height)
            self.rect.x = random.randint(0, largeur_ecran - self.rect.width)
        elif self.spawn_side == "bottom" and self.rect.y < -self.height:
            self.rect.y = random.randint(
                hauteur_ecran, hauteur_ecran + self.height)
            self.rect.x = random.randint(0, largeur_ecran - self.rect.width)
        elif self.spawn_side == "left" and self.rect.x > largeur_ecran:
            self.rect.y = random.randint(0, hauteur_ecran - self.rect.height)
            self.rect.x = random.randint(-largeur_ecran, -self.rect.width)
        elif self.spawn_side == "right" and self.rect.x < -self.width:
            self.rect.y = random.randint(0, hauteur_ecran - self.rect.height)
            self.rect.x = random.randint(
                largeur_ecran, largeur_ecran + self.width)

# Classe pour les ennemis qui se déplacent en diagonale (en haut à gauche, en haut à droite, en bas à gauche, en bas à droite)


class BonusVie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 30
        self.height = 30
        self.color = (0, 0, 255)
        self.rect = pygame.Rect(random.randint(0, largeur_ecran - self.width),
                                random.randint(0, hauteur_ecran - self.height), self.width, self.height)
        self.spawn_time = time.time() + random.randint(10, 50)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class EnnemiFort(Ennemi):
    def __init__(self, target):
        super().__init__(target)
        self.vies = random.randint(2, 5)
        self.color = (255 - 50 * self.vies, 0, 0)

    def update(self):
        super().update()
        if self.vies <= 0:
            self.rect.y = random.randint(-hauteur_ecran, -self.rect.height)
            self.rect.x = random.randint(0, largeur_ecran - self.rect.width)
            self.speed_factor = random.uniform(0.5, 1)
            self.vies = random.randint(2, 5)
        self.color = (255 - 50 * self.vies, 0, 0)


def main():
    horloge = pygame.time.Clock()
    vaisseau = Vaisseau()
    ennemis = [Ennemi(vaisseau) for _ in range(nb_ennemis // 2)] + \
        [EnnemiFort(vaisseau) for _ in range(nb_ennemis // 2)]
    tirs = []
    score = 0
    vies = 3
    bonus_vie = BonusVie()
    run = True
    while run:
        horloge.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                dx = mouseX - vaisseau.rect.centerx
                dy = mouseY - vaisseau.rect.centery
                dist = math.sqrt(dx * dx + dy * dy)
                tir = Tir(vaisseau.rect.centerx,
                          vaisseau.rect.centery, dx / dist, dy / dist)
                tirs.append(tir)

        vaisseau.update(keys)
        for tir in tirs:
            tir.update()

        for ennemi in ennemis:
            ennemi.update()

        # Mise à jour des ennemis forts
            for ennemi in ennemis:
                if vaisseau.rect.colliderect(ennemi.rect):
                    ennemis.remove(ennemi)
                    ennemis.append(Ennemi(vaisseau))
                    vies -= 1
                    if not vaisseau.clignotement:  # Ajoutez cette ligne
                        vaisseau.clignotement = True  # Ajoutez cette ligne
                        vaisseau.clignotement_timer = time.time()  # Ajoutez cette ligne
                        vaisseau.clignotement_start = time.time()

                if vaisseau.clignotement and time.time() - vaisseau.clignotement_start > 2:
                    vaisseau.clignotement = False
                    vaisseau.color = VERT
        # Supprime les tirs hors de l'écran
        tirs[:] = [tir for tir in tirs if 0 <= tir.rect.x <=
                   largeur_ecran and 0 <= tir.rect.y <= hauteur_ecran]

        # Collision entre les tirs et les ennemis
        for tir in tirs:
            for ennemi in ennemis:
                if tir.rect.colliderect(ennemi.rect):
                    tirs.remove(tir)
                    ennemis.remove(ennemi)
                    ennemis.append(Ennemi(vaisseau))
                    score += 100
                    break

        # Collision entre les tirs et les ennemis forts
        for tir in tirs:
            for ennemi in ennemis:
                if tir.rect.colliderect(ennemi.rect):
                    tirs.remove(tir)
                    ennemi.vies -= 1
                    ennemi.color = ennemi.get_color_from_vies(ennemi.vies)
                    if ennemi.vies <= 0:
                        ennemis.remove(ennemi)
                        ennemis.append(Ennemi(vaisseau))
                        score += 100
                    break

        # Collision entre le vaisseau et les ennemis
        for ennemi in ennemis:
            if vaisseau.rect.colliderect(ennemi.rect):
                ennemis.remove(ennemi)
                ennemis.append(Ennemi(vaisseau))
                vies -= 1

        # Collision entre le vaisseau et les bonus de vie
        if vaisseau.rect.colliderect(bonus_vie.rect) and time.time() >= bonus_vie.spawn_time:
            vies += 1
            bonus_vie.rect.x = random.randint(
                0, largeur_ecran - bonus_vie.width)
            bonus_vie.rect.y = random.randint(
                0, hauteur_ecran - bonus_vie.height)
            bonus_vie.spawn_time = time.time() + random.randint(10, 50)

        if vies <= 0:
            run = False

        # Dessine les éléments du jeu
        ecran.fill(NOIR)
        vaisseau.draw(ecran)
        for tir in tirs:
            tir.draw(ecran)
        for ennemi in ennemis:
            ennemi.draw(ecran)

        # Dessine le bonus de vie s'il est prêt à apparaître
        if time.time() >= bonus_vie.spawn_time:
            bonus_vie.draw(ecran)

        # Affiche le score et le nombre de vies
        score_text = police.render(f"Score: {score}", True, BLANC)
        vies_text = police.render(f"Vies: {vies}", True, BLANC)
        ecran.blit(score_text, (10, 10))
        ecran.blit(vies_text, (largeur_ecran - 100, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
