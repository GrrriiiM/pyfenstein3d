//go:build !windows

package game

// SetFont is a no-op on non-Windows platforms.
func SetFont(_ int16, _ string) {}

// Resize sends the ANSI escape sequence to resize the terminal to (x, y) cells.
func Resize(xSize, ySize int) {
	print("\x1b[8;" + itoa(ySize) + ";" + itoa(xSize) + "t")
}

// EnableVirtualTerminal is a no-op on non-Windows platforms (VT is always on).
func EnableVirtualTerminal() {}

func itoa(n int) string {
	if n == 0 {
		return "0"
	}
	buf := [20]byte{}
	pos := len(buf)
	for n > 0 {
		pos--
		buf[pos] = byte('0' + n%10)
		n /= 10
	}
	return string(buf[pos:])
}
