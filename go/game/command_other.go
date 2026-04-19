//go:build !windows

package game

// ServerInput is the interface through which Command drives the game server.
type ServerInput interface {
	PlayerStartMovingFront(id string)
	PlayerStartMovingBack(id string)
	PlayerStartMovingLeft(id string)
	PlayerStartMovingRight(id string)
	PlayerStartTurningLeft(id string)
	PlayerStartTurningRight(id string)
	PlayerStartShooting(id string)
	PlayerStartInteracting(id string)
	PlayerStopMovingFront(id string)
	PlayerStopMovingBack(id string)
	PlayerStopMovingLeft(id string)
	PlayerStopMovingRight(id string)
	PlayerStopTurningLeft(id string)
	PlayerStopTurningRight(id string)
	PlayerStopShooting(id string)
	PlayerStopInteracting(id string)
}

// Command reads keyboard input and forwards it to the server.
// On non-Windows platforms this is a stub that prints a notice.
type Command struct{}

// NewCommand creates a new keyboard Command handler.
func NewCommand() *Command { return &Command{} }

// Apply is a no-op on non-Windows platforms (keyboard detection requires Windows).
func (c *Command) Apply(_ ServerInput) {}
