package engine

import (
	"os"
	"sync"
	"time"
)

// MapInterface allows Map2d to be mocked in tests.
type MapInterface interface {
	Update(deltaTime float64)
	GetPlayer(playerID string) *Player
}

// Server manages the game loop in a background goroutine.
type Server struct {
	map2d        MapInterface
	gameIsRunning bool
	FrameCount   int
	deltaTime    float64
	mu           sync.Mutex
	wg           sync.WaitGroup

	// Injectable dependencies for testing.
	ReadFile  func(path string) (string, error)
	CreateMap func(pattern string) MapInterface
}

// NewServer creates a new Server with default dependencies.
func NewServer() *Server {
	s := &Server{}
	s.ReadFile = func(path string) (string, error) {
		data, err := os.ReadFile(path)
		if err != nil {
			return "", err
		}
		return string(data), nil
	}
	s.CreateMap = func(pattern string) MapInterface {
		return CreateWithPattern(pattern)
	}
	return s
}

// LoadMapFile reads a map pattern file and initialises the map.
func (s *Server) LoadMapFile(filePath string) error {
	content, err := s.ReadFile(filePath)
	if err != nil {
		return err
	}
	s.map2d = s.CreateMap(content)
	return nil
}

// StartGame launches the game loop goroutine. It blocks until the loop exits.
func (s *Server) StartGame() {
	s.mu.Lock()
	if s.gameIsRunning {
		s.mu.Unlock()
		return
	}
	s.gameIsRunning = true
	s.mu.Unlock()

	s.wg.Add(1)
	go func() {
		defer s.wg.Done()
		s.loop()
	}()
	s.wg.Wait()
}

// StopGame signals the game loop to stop.
func (s *Server) StopGame() {
	s.mu.Lock()
	s.gameIsRunning = false
	s.mu.Unlock()
}

// Update performs a single game tick with the given delta time.
func (s *Server) Update(deltaTime float64) {
	s.deltaTime = deltaTime
	s.map2d.Update(s.deltaTime)
}

func (s *Server) loop() {
	s.FrameCount++
	loopTime := 1.0 / float64(FramePerSeconds)
	for {
		s.mu.Lock()
		running := s.gameIsRunning
		s.mu.Unlock()
		if !running {
			break
		}
		start := time.Now()
		s.Update(loopTime)
		elapsed := time.Since(start).Seconds()
		s.deltaTime = elapsed
		sleep := loopTime - elapsed
		if sleep > 0 {
			time.Sleep(time.Duration(sleep * float64(time.Second)))
		}
	}
}

// GetPlayerState returns the player with the given ID.
func (s *Server) GetPlayerState(playerID string) *Player {
	return s.map2d.GetPlayer(playerID)
}

func (s *Server) PlayerStartMovingFront(playerID string) {
	s.map2d.GetPlayer(playerID).IsMovingFront = true
}
func (s *Server) PlayerStartMovingBack(playerID string) {
	s.map2d.GetPlayer(playerID).IsMovingBack = true
}
func (s *Server) PlayerStartMovingRight(playerID string) {
	s.map2d.GetPlayer(playerID).IsMovingRight = true
}
func (s *Server) PlayerStartMovingLeft(playerID string) {
	s.map2d.GetPlayer(playerID).IsMovingLeft = true
}
func (s *Server) PlayerStartTurningRight(playerID string) {
	s.map2d.GetPlayer(playerID).IsTurningRight = true
}
func (s *Server) PlayerStartTurningLeft(playerID string) {
	s.map2d.GetPlayer(playerID).IsTurningLeft = true
}
func (s *Server) PlayerStartInteracting(playerID string) {
	s.map2d.GetPlayer(playerID).IsInteracting = true
}
func (s *Server) PlayerStartShooting(playerID string) {
	s.map2d.GetPlayer(playerID).weapon.IsShooting = true
}
func (s *Server) PlayerStopMovingFront(playerID string) {
	s.map2d.GetPlayer(playerID).IsMovingFront = false
}
func (s *Server) PlayerStopMovingBack(playerID string) {
	s.map2d.GetPlayer(playerID).IsMovingBack = false
}
func (s *Server) PlayerStopMovingRight(playerID string) {
	s.map2d.GetPlayer(playerID).IsMovingRight = false
}
func (s *Server) PlayerStopMovingLeft(playerID string) {
	s.map2d.GetPlayer(playerID).IsMovingLeft = false
}
func (s *Server) PlayerStopTurningRight(playerID string) {
	s.map2d.GetPlayer(playerID).IsTurningRight = false
}
func (s *Server) PlayerStopTurningLeft(playerID string) {
	s.map2d.GetPlayer(playerID).IsTurningLeft = false
}
func (s *Server) PlayerStopInteracting(playerID string) {
	s.map2d.GetPlayer(playerID).IsInteracting = false
}
func (s *Server) PlayerStopShooting(playerID string) {
	s.map2d.GetPlayer(playerID).weapon.IsShooting = false
}
