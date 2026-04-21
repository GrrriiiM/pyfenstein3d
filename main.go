package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"

	"pyfenstein3d/engine"
	"pyfenstein3d/game"
)

func main() {
	// Resolve the asset base directory relative to the executable so the binary
	// can be run from any working directory, matching Python's
	//   os.path.dirname(__file__)/../maps_pattern/map_1_level_1.txt
	// and
	//   os.path.dirname(__file__)/../imgs/walls.png
	// patterns in the original source.
	_, selfFile, _, ok := runtime.Caller(0)
	if !ok {
		fmt.Fprintln(os.Stderr, "error: could not determine source path")
		os.Exit(1)
	}
	// selfFile is the absolute path to main.go at compile time; the pyfenstein3d
	// module root is its parent directory (go/).  The Python assets live one
	// level further up in pyfenstein3d/ (relative to the repo root), which is
	// ../pyfenstein3d from the go/ directory.
	goDir := filepath.Dir(selfFile)
	assetsDir := filepath.Join(goDir, "..", "pyfenstein3d")

	game.PrepareConsole()

	img, err := game.NewImage(assetsDir)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error loading sprites: %v\n", err)
		os.Exit(1)
	}

	hudPath := filepath.Join(assetsDir, "imgs", "hud.png")
	screen, err := game.NewScreen(img, hudPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error creating screen: %v\n", err)
		os.Exit(1)
	}

	server := engine.NewServer()
	command := game.NewCommand()

	mapFile := filepath.Join(assetsDir, "maps_pattern", "map_1_level_1.txt")
	g, err := game.NewGame(command, screen, server, mapFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error loading map: %v\n", err)
		os.Exit(1)
	}

	g.Start()
}
