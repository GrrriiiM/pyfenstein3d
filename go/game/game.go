package game

import (
	"fmt"
	"os"
	"time"

	"pyfenstein3d/engine"
)

// GameServer is the interface the Game needs from the engine server.
type GameServer interface {
	ServerInput
	LoadMapFile(filePath string) error
	Update(deltaTime float64)
	GetPlayerState(playerID string) *engine.Player
}

// Game ties together the engine server, keyboard command handler and screen renderer.
type Game struct {
	command    *Command
	screen     *Screen
	server     GameServer
	frameCount int
}

// NewGame creates a new Game. mapFile is the path to the map pattern file;
// it is loaded immediately during construction.
func NewGame(command *Command, screen *Screen, server GameServer, mapFile string) (*Game, error) {
	if err := server.LoadMapFile(mapFile); err != nil {
		return nil, err
	}
	g := &Game{
		command: command,
		screen:  screen,
		server:  server,
	}
	return g, nil
}

// PrepareConsole prints the key-bindings help text, resizes the terminal and
// clears the screen — mirroring Python's Game.prepare_console().
func PrepareConsole() {
	EnableVirtualTerminal()
	fmt.Println("COMANDOS")
	fmt.Println("- Andar para frente: W")
	fmt.Println("- Andar para trás: S")
	fmt.Println("- Andar para esquerda: A")
	fmt.Println("- Andar para direita: D")
	fmt.Println("- Virar para esquerda: Seta esquerda")
	fmt.Println("- Virar para direita: Seta direta")
	fmt.Println("- Atirar: Seta cima")
	fmt.Println("- Abrir porta: Espaço")
	fmt.Println()
	fmt.Println("As configurações do seu console serão alteradas:")
	fmt.Println("LARGURA: 200")
	fmt.Println("ALTURA: 62")
	fmt.Println("FONTE: Consolas 5px")
	fmt.Println()
	fmt.Print("Pressione ENTER para começar")
	fmt.Scanln() //nolint:errcheck
	SetFont(5, "Consolas")
	Resize(200, 62)
	fmt.Print("\033[2J\033[H") // cls
}

// Start runs the main game loop, mirroring Python's Game.start().
func (g *Game) Start() {
	g.frameCount++
	loopTime := 1.0 / float64(engine.FramePerSeconds)

	g.screen.DrawHUD()

	for {
		startTime := time.Now()
		g.command.Apply(g.server)
		g.server.Update(loopTime)
		state := g.server.GetPlayerState("123")
		g.screen.Draw(state)
		elapsed := time.Since(startTime).Seconds()
		if elapsed < loopTime {
			time.Sleep(time.Duration((loopTime - elapsed) * float64(time.Second)))
			elapsed = loopTime
		}
		fmt.Fprintf(os.Stderr, "\033]0;Pyfenstein3d - frame: %04.1f - health: %03.0f - ammo: %03.0f - score: %d\007",
			1/elapsed, float64(state.Health()), float64(state.Ammo()), state.Score())
	}
}
