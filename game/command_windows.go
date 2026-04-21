//go:build windows

package game

// Virtual-key codes used by the game.
const (
	vkLeft  = 0x25 // VK_LEFT
	vkRight = 0x27 // VK_RIGHT
	vkUp    = 0x26 // VK_UP
	vkW     = 0x57
	vkS     = 0x53
	vkA     = 0x41
	vkD     = 0x44
	vkSpace = 0x20
)

var procGetAsyncKeyState = kernel32.NewProc("GetAsyncKeyState")

// isPressed reports whether the virtual key identified by vk is currently held.
func isPressed(vk uintptr) bool {
	// GetAsyncKeyState returns a SHORT; the high-order bit is set if the key is down.
	r, _, _ := procGetAsyncKeyState.Call(vk)
	return int16(r) < 0
}

// Command reads the keyboard state and forwards it to the server on each Apply call.
type Command struct{}

// NewCommand creates a new keyboard Command handler.
func NewCommand() *Command { return &Command{} }

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

// Apply reads the current keyboard state and calls the corresponding server methods.
func (c *Command) Apply(server ServerInput) {
	const pid = "123"

	server.PlayerStopTurningLeft(pid)
	server.PlayerStopTurningRight(pid)
	server.PlayerStopShooting(pid)
	server.PlayerStopMovingFront(pid)
	server.PlayerStopMovingBack(pid)
	server.PlayerStopMovingLeft(pid)
	server.PlayerStopMovingRight(pid)
	server.PlayerStopInteracting(pid)

	if isPressed(vkLeft) {
		server.PlayerStartTurningLeft(pid)
	}
	if isPressed(vkRight) {
		server.PlayerStartTurningRight(pid)
	}
	if isPressed(vkUp) {
		server.PlayerStartShooting(pid)
	}
	if isPressed(vkW) {
		server.PlayerStartMovingFront(pid)
	}
	if isPressed(vkS) {
		server.PlayerStartMovingBack(pid)
	}
	if isPressed(vkA) {
		server.PlayerStartMovingLeft(pid)
	}
	if isPressed(vkD) {
		server.PlayerStartMovingRight(pid)
	}
	if isPressed(vkSpace) {
		server.PlayerStartInteracting(pid)
	}
}
