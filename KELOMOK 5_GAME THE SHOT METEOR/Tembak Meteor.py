import pygame
import random

# Inisialisasi pygame
pygame.init()

# Kelas Game
class GameTembakMeteor:
    def __init__(self):
        # Dimensi layar
        self.lebar_layar = 800
        self.tinggi_layar = 600
        self.layar = pygame.display.set_mode((self.lebar_layar, self.tinggi_layar))
        pygame.display.set_caption("Game Tembak Meteor")
        
        # Warna
        self.warna_latar = (0, 0, 30)  # Biru gelap
        self.warna_peluru = (255, 255, 0)  # Putih
        self.warna_meteor = (200, 0, 0)  # Kuning

        # Memuat gambar dan menyesuaikan ukurannya
        try:
            self.gambar_pemain = pygame.image.load("pemain.png")  # Gambar pemain
            self.gambar_peluru = pygame.image.load("peluru.png")  # Gambar peluru
            self.gambar_meteor = pygame.image.load("meteor.png")  # Gambar meteor
            self.gambar_background = pygame.image.load("background.jpg")  # Gambar latar belakang
            
            # Menyesuaikan ukuran gambar
            self.gambar_pemain = pygame.transform.scale(self.gambar_pemain, (85, 85))  # Ukuran pemain
            self.gambar_peluru = pygame.transform.scale(self.gambar_peluru, (35, 35))  # Ukuran peluru
            self.gambar_meteor = pygame.transform.scale(self.gambar_meteor, (50, 50))  # Ukuran meteor
            self.gambar_background = pygame.transform.scale(self.gambar_background, (self.lebar_layar, self.tinggi_layar))  # Ukuran background
            
        except pygame.error as e:
            print(f"Error loading image: {e}")
        
        # Pemain
        self.pemain = pygame.Rect(self.lebar_layar // 2 - 25, self.tinggi_layar - 60, 50, 50)  # Posisi pemain
        self.kecepatan_pemain = 10
        
        # Peluru
        self.peluru = None
        self.kecepatan_peluru = 85
        
        # Meteor
        self.meteor = pygame.Rect(random.randint(0, self.lebar_layar - 30), 0, 30, 30)  # Posisi meteor
        self.kecepatan_meteor = 3
        
        # Skor
        self.skor = 0
        self.font = pygame.font.Font(None, 36)
        self.font_game_over = pygame.font.Font(None, 72)  # Font untuk Game Over
        
        # Status permainan
        self.berjalan = True
        self.game_over = False

         # Memuat audio
        pygame.mixer.init()
        self.sfx_shoot = pygame.mixer.Sound("shoot.wav")  # Suara tembakan
        self.sfx_explosion = pygame.mixer.Sound("ledakan.mp3")  # Suara ledakan
        self.music = pygame.mixer.music.load("background.mp3")  # Musik latar
        pygame.mixer.music.play(-1, 0.0)  # Mainkan musik latar secara berulang

    def tampilkan_skor(self):
        teks_skor = self.font.render(f"Skor: {self.skor}", True, (255, 255, 255))
        self.layar.blit(teks_skor, (10, 10))

    def tampilkan_game_over(self):
        teks_game_over = self.font_game_over.render("GAME OVER", True, (255, 0, 0))
        instruksi = self.font.render("Tekan R untuk Restart atau Q untuk Keluar", True, (255, 255, 255))
        self.layar.blit(teks_game_over, (self.lebar_layar // 2 - teks_game_over.get_width() // 2, self.tinggi_layar // 3))
        self.layar.blit(instruksi, (self.lebar_layar // 2 - instruksi.get_width() // 2, self.tinggi_layar // 2))

    def mainkan(self):
        clock = pygame.time.Clock()
        
        while self.berjalan:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.berjalan = False
            
            if self.game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:  # Restart permainan
                    self.game_over = False
                    self.skor = 0
                    self.meteor.y = 0
                    self.meteor.x = random.randint(0, self.lebar_layar - 30)
                elif keys[pygame.K_q]:  # Keluar dari permainan
                    self.berjalan = False
            else:
                # Kontrol pemain
                tombol = pygame.key.get_pressed()
                
                # Gerakan kiri-kanan
                if tombol[pygame.K_LEFT] and self.pemain.left > 0:
                    self.pemain.x -= self.kecepatan_pemain
                if tombol[pygame.K_RIGHT] and self.pemain.right < self.lebar_layar:
                    self.pemain.x += self.kecepatan_pemain
                
                # Gerakan atas-bawah
                if tombol[pygame.K_UP] and self.pemain.top > 0:
                    self.pemain.y -= self.kecepatan_pemain
                if tombol[pygame.K_DOWN] and self.pemain.bottom < self.tinggi_layar:
                    self.pemain.y += self.kecepatan_pemain
                
                if tombol[pygame.K_SPACE] and self.peluru is None:
                    self.peluru = pygame.Rect(self.pemain.centerx - 5, self.pemain.top, 10, 20)
                    self.sfx_shoot.play()  # Suara tembakan
                
                # Update peluru
                if self.peluru:
                    self.peluru.y -= self.kecepatan_peluru
                    if self.peluru.colliderect(self.meteor):
                        self.skor += 1
                        self.meteor.y = 0
                        self.meteor.x = random.randint(0, self.lebar_layar - 30)
                        self.peluru = None
                        self.sfx_explosion.play()  # Suara ledakan
                    elif self.peluru.y < 0:
                        self.peluru = None
                
                # Update meteor
                self.meteor.y += self.kecepatan_meteor
                if self.meteor.y > self.tinggi_layar:
                    self.game_over = True
            
            # Gambar layar
            self.layar.blit(self.gambar_background, (0, 0))  # Background
            self.layar.blit(self.gambar_pemain, self.pemain)  # Pemain
            self.layar.blit(self.gambar_meteor, self.meteor)  # Meteor
            if self.peluru:
                self.layar.blit(self.gambar_peluru, self.peluru)  # Peluru
            
            if self.game_over:
                self.tampilkan_game_over()
            else:
                self.tampilkan_skor()
            
            pygame.display.flip()
            clock.tick(30)

# Jalankan game
if __name__ == "__main__":
    game = GameTembakMeteor()
    game.mainkan()
    pygame.quit()
