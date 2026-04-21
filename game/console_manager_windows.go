//go:build windows

package game

import (
	"unsafe"

	"golang.org/x/sys/windows"
)

var (
	kernel32           = windows.NewLazySystemDLL("kernel32.dll")
	procGetStdHandle   = kernel32.NewProc("GetStdHandle")
	procGetCurrentConsoleFontEx = kernel32.NewProc("GetCurrentConsoleFontEx")
	procSetConsoleFontEx = kernel32.NewProc("SetCurrentConsoleFontEx")
	procSetConsoleMode = kernel32.NewProc("SetConsoleMode")
)

const (
	stdOutputHandle                  = ^uintptr(10) // -11 as uintptr
	enableVirtualTerminalProcessing  = 0x0004
	lfFaceSize                       = 32
)

type coord struct {
	X, Y int16
}

type consoleFontInfoEx struct {
	CbSize    uint32
	NFont     uint32
	DwFontSize coord
	FontFamily uint32
	FontWeight uint32
	FaceName  [lfFaceSize]uint16
}

// SetFont sets the Windows console font to the given size and face name.
func SetFont(fontSize int16, fontFamily string) {
	h, _, _ := procGetStdHandle.Call(stdOutputHandle)
	if h == 0 {
		return
	}
	fi := consoleFontInfoEx{}
	fi.CbSize = uint32(unsafe.Sizeof(fi))
	fi.DwFontSize.X = fontSize
	fi.DwFontSize.Y = fontSize
	face := windows.StringToUTF16(fontFamily)
	for i, v := range face {
		if i >= lfFaceSize {
			break
		}
		fi.FaceName[i] = v
	}
	procSetConsoleFontEx.Call(h, 0, uintptr(unsafe.Pointer(&fi))) //nolint:errcheck
}

// Resize sends the ANSI escape sequence to resize the terminal to (x, y) cells.
func Resize(xSize, ySize int) {
	// The Python code uses print(f"\x1b[8;{y_size};{x_size}t")
	print("\x1b[8;" + itoa(ySize) + ";" + itoa(xSize) + "t")
}

// EnableVirtualTerminal enables ANSI/VT processing on the Windows console
// stdout handle so that escape codes are interpreted by the terminal.
func EnableVirtualTerminal() {
	h, _, _ := procGetStdHandle.Call(stdOutputHandle)
	if h == 0 {
		return
	}
	var mode uint32
	windows.GetConsoleMode(windows.Handle(h), &mode)
	windows.SetConsoleMode(windows.Handle(h), mode|enableVirtualTerminalProcessing)
}

// itoa converts a non-negative integer to its decimal string without importing
// strconv (avoids an extra import just for this helper).
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
