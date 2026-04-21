package engine

import (
	"testing"
)

// mockMap is a simple MapInterface implementation for testing.
type mockMap struct {
	updateFunc   func(float64)
	getPlayerFn  func(string) *Player
}

func (m *mockMap) Update(deltaTime float64) {
	if m.updateFunc != nil {
		m.updateFunc(deltaTime)
	}
}

func (m *mockMap) GetPlayer(playerID string) *Player {
	if m.getPlayerFn != nil {
		return m.getPlayerFn(playerID)
	}
	return nil
}

func TestServerInit(t *testing.T) {
	server := NewServer()

	fileOpenedWith := ""
	server.ReadFile = func(path string) (string, error) {
		fileOpenedWith = path
		return "010203", nil
	}

	updateCount := 0
	mm := &mockMap{}
	mm.updateFunc = func(deltaTime float64) {
		updateCount++
		server.StopGame()
	}

	server.CreateMap = func(pattern string) MapInterface {
		return mm
	}

	if err := server.LoadMapFile("teste"); err != nil {
		t.Fatalf("LoadMapFile failed: %v", err)
	}

	server.StartGame()

	if fileOpenedWith != "teste" {
		t.Errorf("expected file opened with 'teste', got '%s'", fileOpenedWith)
	}
	if updateCount != 1 {
		t.Errorf("expected update called once, got %d", updateCount)
	}
}
