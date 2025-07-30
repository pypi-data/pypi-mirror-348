/*
  GladUI (GUI library for python to create games)
  GladGamingStudio 2025-26, Navthej
  
  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.

*/

/*
  The main code of GladUI, all functions included.
  To make this code work fine, do not delete assets folder (assets/), it contains some files which had been used in this main code.
*/

#include <Python.h>
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
#include <unordered_map>
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>

#include "assets/GladG/GladG.h"

#define MajorVersion 0
#define MinorVersion 8
#define PatchVersion 0

using namespace std;

//main variables
SDL_Window *window;
SDL_Renderer *renderer;
SDL_Event event;

int geometry_x, geometry_y;

bool WindowShouldAlive = true;
bool WindowShouldResize = false;
bool AutoClose = true;
bool QUIT = false;

Uint8 BgR, BgG, BgB, BgA;

unordered_map<string, SDL_Texture*> images;
unordered_map<string, Mix_Music*> musics;
unordered_map<string, Mix_Chunk*> bgmS;

//KEYS
unordered_map<string, SDL_Scancode> 
keymap = {
    // Numbers
    {"1", SDL_SCANCODE_1}, {"2", SDL_SCANCODE_2}, {"3", SDL_SCANCODE_3},
    {"4", SDL_SCANCODE_4}, {"5", SDL_SCANCODE_5}, {"6", SDL_SCANCODE_6},
    {"7", SDL_SCANCODE_7}, {"8", SDL_SCANCODE_8}, {"9", SDL_SCANCODE_9},
    {"0", SDL_SCANCODE_0},

    // Letters
    {"A", SDL_SCANCODE_A}, {"B", SDL_SCANCODE_B}, {"C", SDL_SCANCODE_C},
    {"D", SDL_SCANCODE_D}, {"E", SDL_SCANCODE_E}, {"F", SDL_SCANCODE_F},
    {"G", SDL_SCANCODE_G}, {"H", SDL_SCANCODE_H}, {"I", SDL_SCANCODE_I},
    {"J", SDL_SCANCODE_J}, {"K", SDL_SCANCODE_K}, {"L", SDL_SCANCODE_L},
    {"M", SDL_SCANCODE_M}, {"N", SDL_SCANCODE_N}, {"O", SDL_SCANCODE_O},
    {"P", SDL_SCANCODE_P}, {"Q", SDL_SCANCODE_Q}, {"R", SDL_SCANCODE_R},
    {"S", SDL_SCANCODE_S}, {"T", SDL_SCANCODE_T}, {"U", SDL_SCANCODE_U},
    {"V", SDL_SCANCODE_V}, {"W", SDL_SCANCODE_W}, {"X", SDL_SCANCODE_X},
    {"Y", SDL_SCANCODE_Y}, {"Z", SDL_SCANCODE_Z},

    // Arrows
    {"UP", SDL_SCANCODE_UP}, {"DOWN", SDL_SCANCODE_DOWN},
    {"LEFT", SDL_SCANCODE_LEFT}, {"RIGHT", SDL_SCANCODE_RIGHT},

    // Modifiers
    {"LCTRL", SDL_SCANCODE_LCTRL}, {"RCTRL", SDL_SCANCODE_RCTRL},
    {"LSHIFT", SDL_SCANCODE_LSHIFT}, {"RSHIFT", SDL_SCANCODE_RSHIFT},
    {"LALT", SDL_SCANCODE_LALT}, {"RALT", SDL_SCANCODE_RALT},
    {"LGUI", SDL_SCANCODE_LGUI}, {"RGUI", SDL_SCANCODE_RGUI},

    // Function keys
    {"F1", SDL_SCANCODE_F1}, {"F2", SDL_SCANCODE_F2}, {"F3", SDL_SCANCODE_F3},
    {"F4", SDL_SCANCODE_F4}, {"F5", SDL_SCANCODE_F5}, {"F6", SDL_SCANCODE_F6},
    {"F7", SDL_SCANCODE_F7}, {"F8", SDL_SCANCODE_F8}, {"F9", SDL_SCANCODE_F9},
    {"F10", SDL_SCANCODE_F10}, {"F11", SDL_SCANCODE_F11}, {"F12", SDL_SCANCODE_F12},

    // Symbols and others
    {"SPACE", SDL_SCANCODE_SPACE},
    {"RETURN", SDL_SCANCODE_RETURN}, {"ENTER", SDL_SCANCODE_RETURN},
    {"ESCAPE", SDL_SCANCODE_ESCAPE}, {"TAB", SDL_SCANCODE_TAB},
    {"BACKSPACE", SDL_SCANCODE_BACKSPACE},
    {"CAPSLOCK", SDL_SCANCODE_CAPSLOCK},
    {"MINUS", SDL_SCANCODE_MINUS}, {"EQUALS", SDL_SCANCODE_EQUALS},
    {"LEFTBRACKET", SDL_SCANCODE_LEFTBRACKET},
    {"RIGHTBRACKET", SDL_SCANCODE_RIGHTBRACKET},
    {"BACKSLASH", SDL_SCANCODE_BACKSLASH},
    {"SEMICOLON", SDL_SCANCODE_SEMICOLON},
    {"APOSTROPHE", SDL_SCANCODE_APOSTROPHE},
    {"GRAVE", SDL_SCANCODE_GRAVE},
    {"COMMA", SDL_SCANCODE_COMMA},
    {"PERIOD", SDL_SCANCODE_PERIOD},
    {"SLASH", SDL_SCANCODE_SLASH},

    // Numpad
    {"NUM_0", SDL_SCANCODE_KP_0}, {"NUM_1", SDL_SCANCODE_KP_1},
    {"NUM_2", SDL_SCANCODE_KP_2}, {"NUM_3", SDL_SCANCODE_KP_3},
    {"NUM_4", SDL_SCANCODE_KP_4}, {"NUM_5", SDL_SCANCODE_KP_5},
    {"NUM_6", SDL_SCANCODE_KP_6}, {"NUM_7", SDL_SCANCODE_KP_7},
    {"NUM_8", SDL_SCANCODE_KP_8}, {"NUM_9", SDL_SCANCODE_KP_9},
    {"NUM_PLUS", SDL_SCANCODE_KP_PLUS},
    {"NUM_MINUS", SDL_SCANCODE_KP_MINUS},
    {"NUM_MULTIPLY", SDL_SCANCODE_KP_MULTIPLY},
    {"NUM_DIVIDE", SDL_SCANCODE_KP_DIVIDE},
    {"NUM_ENTER", SDL_SCANCODE_KP_ENTER},
    {"NUM_PERIOD", SDL_SCANCODE_KP_PERIOD}
};
//MOUSE
unordered_map <string, Uint8> mousemap = {
	{"LEFT", SDL_BUTTON_LEFT},
	{"RIGHT", SDL_BUTTON_RIGHT},
	{"MIDDLE", SDL_BUTTON_MIDDLE}
};

//MAIN FUNCTIONS

//GetColor, giveout RGBA.
vector<Uint8> GetColor(PyObject *list)
{
	vector<Uint8> RGBA;
	for (int i = 0; i < 4; i++)
	{
		RGBA.push_back((Uint8)PyLong_AsLong(PyList_GetItem(list, i)));
	}
	return RGBA;
}

//Init, Initilize...
void INIT()
{
	SDL_Init(SDL_INIT_VIDEO);
	IMG_Init(IMG_INIT_PNG | IMG_INIT_JPG);
	TTF_Init();
}

//Function quit(), breaks the mainloop, destroy everything.
void quit()
{
    WindowShouldAlive = false;
    
    // Free all music
    for (auto& pair : musics) {
        if (pair.second) {
            Mix_FreeMusic(pair.second);
        }
    }
    musics.clear();
    
    // Free all sounds
    for (auto& pair : bgmS) {
        if (pair.second) {
            Mix_FreeChunk(pair.second);
        }
    }
    bgmS.clear();

	//CloseAudio
    Mix_CloseAudio();

    //Destroy renderer
    if (renderer) SDL_DestroyRenderer(renderer);

    //Destroy window
    if (window) SDL_DestroyWindow(window);
    SDL_Quit();
}

void ExtractFromList(int &x, int &y,  int &width, int &height, float &rad, PyObject *python_list)
{
	if (PyList_Check(python_list))
	{
		PyObject *xObj = PyList_GetItem(python_list, 0);
		PyObject *yObj = PyList_GetItem(python_list, 1);
		//assign, now only x and y.
		if (PyLong_Check(xObj)) x = PyLong_AsLong(xObj);
		if (PyLong_Check(yObj)) y = PyLong_AsLong(yObj);

		//checking if it's rect or circle
		if (PyList_Size(python_list) == 4)
		{
			PyObject *widthObj = PyList_GetItem(python_list, 2);
			PyObject *heightObj = PyList_GetItem(python_list, 3);
			
			if (PyLong_Check(widthObj)) width = PyLong_AsLong(widthObj);
			if (PyLong_Check(heightObj)) height = PyLong_AsLong(heightObj);
		}
		// if circle
		else if (PyList_Size(python_list) == 3)
		{
			PyObject *radObj = PyList_GetItem(python_list, 2);

			if (PyLong_Check(radObj)) rad = PyLong_AsLong(radObj);
		}
	}
}

//--Helper functions end from HERE--

//--THE PYTHON FUNCTIONS STARTS FROM HERE--

//function version(), returns the version of GladUI
static PyObject *version(PyObject *self, PyObject *args)
{
	string version = to_string(MajorVersion) + "." +
			to_string(MinorVersion) + "." +
			to_string(PatchVersion);

	return Py_BuildValue("s", version.c_str());
}

//--MAIN GUI FUNCTIONS STARTS FROM HERE--

//Function InitAudioDevice(), to initilize the audio.
static PyObject *InitAudioDevice(PyObject *self, PyObject *args)
{
    if(Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 2048) < 0) {
        PyErr_SetString(PyExc_RuntimeError, Mix_GetError());
        
        return NULL;
    }

	Mix_AllocateChannels(32);
    
    Py_RETURN_NONE;
}

//Function Mainloop(), if True, the mainloop continues, else not. Use this on the mainloop like, while Mainloop():.
static PyObject *Mainloop(PyObject *self, PyObject *args)
{
	char mode = WindowShouldAlive;
	return Py_BuildValue("b", mode);
}

/*
  Function SetFPS(fps), set fps as given value. Use this on the mainloop after START() or before END(), like:
    START()
    SetFPS(60)
    ...
    END()
  OR:
	START()
	...
	SetFPS(60)
	END()
*/
static PyObject *SetFPS(PyObject *self, PyObject *args)
{
	int FPS;

	if (!PyArg_ParseTuple(args, "i", &FPS))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : FPS(int)");

		return NULL;
	}

	//set fps
	setFPS(FPS);

	Py_RETURN_NONE;
}

//Function GetFPS(), returns current FPS.
static PyObject *GetFPS(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", getFPS());
}

//Function CreateWindow(name, resolutionX, resolutionY, resizable = true, bgcolor = [77,77,77,255]) name : project name, resolutionX : size X, resolutionY : sizeY, resizable (bool) : if true, app can be resizable), else not!, bgcolor : a list of 4 numbers, R, G, B, A to have the background color.
static PyObject *CreateWindow(PyObject *self, PyObject *args, PyObject *kwargs)
{
	INIT();
	
	const char *title;
	int sizeX, sizeY;
	PyObject *resizableObj;
	PyObject *bgcolorObj;

	static const char *kwlist[] = {"title", "sizeX", "sizeY", "resizableObj", "bgcolorObj", NULL};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "siiOO", (char **) kwlist, &title, &sizeX, &sizeY, &resizableObj, &bgcolorObj))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments: title (str), width (int), height (int), resizable (bool), bgcolor (list)");
		
		return NULL;
	}

	// Resizable flag
	int resizable = PyObject_IsTrue(resizableObj);
	Uint32 flags = SDL_WINDOW_SHOWN;
	if (resizable)
	{
		flags |= SDL_WINDOW_RESIZABLE;

		WindowShouldResize = true;
	}
	//Get Color
	vector<Uint8> RGBA = GetColor(bgcolorObj);
	Uint8 R = RGBA[0], G = RGBA[1], B = RGBA[2], A = RGBA[3];
	BgR = R;
	BgG = G;
	BgB = B;
	BgA = A;
	
	// Create window
	window = SDL_CreateWindow(title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, sizeX, sizeY, flags);
	if (!window)
		return Py_BuildValue("s", SDL_GetError());

	renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
	if (!renderer)
		return Py_BuildValue("s", SDL_GetError());
	if (WindowShouldResize) SDL_RenderSetLogicalSize(renderer, sizeX, sizeY);

	geometry_x = sizeX;
	geometry_y = sizeY;

	Py_RETURN_NONE;
}

//Function START(), Use this at the begening of the mainloop. To make the Bg clear.
static PyObject *START(PyObject *self, PyObject *args)
{
	SDL_SetRenderDrawColor(renderer, BgR, BgG, BgB, BgA);
	SDL_RenderClear(renderer);

	//check if quit
	while (SDL_PollEvent(&event))
	{
		if (event.type == SDL_QUIT)
		{
			if (AutoClose) quit();
			else QUIT = true;
		}
	}

	Py_RETURN_NONE;
}

//Function END(), Use this at the end of the mainlop. To make all textures make preasent.
static PyObject *END(PyObject *self, PyObject *args)
{
	SDL_RenderPresent(renderer);
	
	QUIT = false;
	
	Py_RETURN_NONE;
}

//Function SetAutoCloseFalse(), set auto close.
static PyObject *SetAutoCloseFalse(PyObject *self, PyObject *args)
{
	AutoClose = false;
	Py_RETURN_NONE;
}

//Function QuitMessage(), returns if the user had pressed close button (to use if used function SetAutoCloseFalse()
static PyObject *QuitMessage(PyObject *self, PyObject *args)
{
	if (AutoClose)
	{
		PyErr_SetString(PyExc_RuntimeError, "Expected using SetAutoCloseFalse() before using QuitMessage()");
		
		return NULL;
	}
	else
	{
		return Py_BuildValue("b", QUIT);
	}
}

//Function Quit(), breaks the mainloop.
static PyObject *Quit(PyObject *self, PyObject *args)
{
	quit();

	Py_RETURN_NONE;
}

//Function Drawtext(text, x, y, size, color, font = "loaded!!"), function to display text on the screen.
static PyObject *DrawText(PyObject *self, PyObject *args, PyObject *kwargs)
{
	const char *text;
	int x, y, size;
	PyObject *color;
	const char *font;

	static const char *kwlist[] = {"text", "x", "y", "size", "color", "font", NULL};

	//error detection
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "siiiOs", (char **)kwlist, &text, &x, &y, &size, &color, &font))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments: text (str), x (int), y (int), size (int), color (list), font (str)");
		
		return NULL;
	}
	if (!font) PyErr_SetString(PyExc_FileNotFoundError, "No font file found.");

	//get color
	vector<Uint8> RGBA = GetColor(color);
	Uint8 R = RGBA[0], G = RGBA[1], B = RGBA[2], A = RGBA[3];
	//setup all
	SDL_Color COLOR = {R, G, B, A};
	VECTOR2 position = {x, y};

	//Draw Text (from GladG.h)
	Drawtext(renderer, font, text, COLOR, position, size);

	Py_RETURN_NONE;
}

//Function Rect(x, y, width, height, color), function to draw a rectangle on the screen
static PyObject *Rect(PyObject *self, PyObject *args, PyObject *kwargs)
{
	int x, y, width, height;
	PyObject *color;

	static const char *kwlist[] = {"x", "y", "width", "height", "color", NULL};

	//Error
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiiiO", (char **)kwlist, &x, &y, &width, &height, &color))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : x(int), y(int), width(int), height(int), color(list)");
		
		return NULL;
	}

	//extract color
	vector<Uint8> RGBA = GetColor(color);
	Uint8 R = RGBA[0], G = RGBA[1], B = RGBA[2], A = RGBA[3];

	//DrawRECT
	SDL_Rect rect = {x, y, width, height};
	SDL_SetRenderDrawColor(renderer, R, G, B, A);
	SDL_RenderFillRect(renderer, &rect);
	
	//Returns x, y, width, height, so that it is easier for the user to use check collusion.
	PyObject *rectangle = PyList_New(4);
	if (!rectangle)
	{
		PyErr_SetString(PyExc_RuntimeError, "Unable to return value.");

		return NULL;
	}

	//setup the variables to add into the list
	PyObject *xObj = PyLong_FromLong(x);
	PyObject *yObj = PyLong_FromLong(y);
	PyObject *widthObj = PyLong_FromLong(width);
	PyObject *heightObj = PyLong_FromLong(height);

	//append to the list
	PyList_SET_ITEM(rectangle, 0, xObj);
	PyList_SET_ITEM(rectangle, 1, yObj);
	PyList_SET_ITEM(rectangle, 2, widthObj);
	PyList_SET_ITEM(rectangle, 3, heightObj);

	return Py_BuildValue("O", rectangle);
}

//Function Circle(x, y, rad, color, fill, fill_color), draws a circle on the screen.
static PyObject *Circle(PyObject *self, PyObject *args, PyObject *kwargs)
{
    int x, y;
    float rad;
    PyObject *color;
    bool fill = false;
    PyObject *fill_color = NULL;

    static const char *kwlist[] = {"x", "y", "rad", "color", "fill", "fill_color", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iifO|bO", (char **)kwlist, 
                                    &x, &y, &rad, &color, &fill, &fill_color))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments: x(int), y(int), radius(float), color(list), [fill(bool)], [fill_color(list)]");
        return NULL;
    }

    // Extract primary color
    vector<Uint8> RGBA = GetColor(color);
    if (RGBA.size() != 4) {
        PyErr_SetString(PyExc_ValueError, "Color must be a list of 4 values [R,G,B,A]");
        return NULL;
    }

    // Extract fill color if provided, else use primary color
    vector<Uint8> fill_RGBA;
    if (fill && fill_color) {
        fill_RGBA = GetColor(fill_color);
        if (fill_RGBA.size() != 4) {
            PyErr_SetString(PyExc_ValueError, "Fill color must be a list of 4 values [R,G,B,A]");
            return NULL;
        }
    } else if (fill) {
        fill_RGBA = RGBA; // Use primary color if no fill color specified
    }

    // Draw outline
    SDL_SetRenderDrawColor(renderer, RGBA[0], RGBA[1], RGBA[2], RGBA[3]);
    
    // Midpoint circle algorithm (optimized for floating-point radius)
    int cx = static_cast<int>(rad - 1);
    int cy = 0;
    float dx = 1;
    float dy = 1;
    float err = dx - (rad * 2);

    while (cx >= cy)
    {
        // Draw 8 symmetric points (octants)
        SDL_RenderDrawPoint(renderer, x + cx, y + cy);
        SDL_RenderDrawPoint(renderer, x + cy, y + cx);
        SDL_RenderDrawPoint(renderer, x - cy, y + cx);
        SDL_RenderDrawPoint(renderer, x - cx, y + cy);
        SDL_RenderDrawPoint(renderer, x - cx, y - cy);
        SDL_RenderDrawPoint(renderer, x - cy, y - cx);
        SDL_RenderDrawPoint(renderer, x + cy, y - cx);
        SDL_RenderDrawPoint(renderer, x + cx, y - cy);

        if (fill) {
            // Draw horizontal lines to fill the circle
            SDL_SetRenderDrawColor(renderer, fill_RGBA[0], fill_RGBA[1], fill_RGBA[2], fill_RGBA[3]);
            SDL_RenderDrawLine(renderer, x - cx, y + cy, x + cx, y + cy);
            SDL_RenderDrawLine(renderer, x - cx, y - cy, x + cx, y - cy);
            SDL_RenderDrawLine(renderer, x - cy, y + cx, x + cy, y + cx);
            SDL_RenderDrawLine(renderer, x - cy, y - cx, x + cy, y - cx);
            SDL_SetRenderDrawColor(renderer, RGBA[0], RGBA[1], RGBA[2], RGBA[3]);
        }

        if (err <= 0) {
            cy++;
            err += dy;
            dy += 2;
        }
        if (err > 0) {
            cx--;
            dx += 2;
            err += dx - (rad * 2);
        }
    }

    // Return circle parameters for collision detection
    PyObject *circle = PyList_New(3);
    if (!circle) {
        PyErr_SetString(PyExc_RuntimeError, "Unable to create return list");
        return NULL;
    }

    PyList_SET_ITEM(circle, 0, PyLong_FromLong(x));
    PyList_SET_ITEM(circle, 1, PyLong_FromLong(y));
    PyList_SET_ITEM(circle, 2, PyFloat_FromDouble(rad));

    return circle;
}

//Function Point(x, y, color), Draws a point to the given position.
static PyObject *Point(PyObject *self, PyObject *args)
{
	int x, y;
	PyObject *color;

	if (!PyArg_ParseTuple(args, "iiO", &x, &y, &color))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : x(int), y(int), color(list)");

		return NULL;
	}

	//Extract color
	vector<Uint8> RGBA = GetColor(color);
	Uint8 R = RGBA[0], G = RGBA[1], B = RGBA[2], A = RGBA[3];

	//Draw
	SDL_SetRenderDrawColor(renderer, R, G, B, A);
	SDL_RenderDrawPoint(renderer, x, y);

	Py_RETURN_NONE;
}

//Function Line(x1, y1, x2, y2, color), Draws a line from (x1, y1) to (x2, y2).
static PyObject *Line(PyObject *self, PyObject *args)
{
	int x1, y1, x2, y2;
	PyObject *color;

	if (!PyArg_ParseTuple(args, "iiiiO", &x1, &y1, &x2, &y2, &color))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : x1, y1, x2, y2 (int) and color(list)");

		return NULL;
	}

	//Extract color
	vector<Uint8> RGBA = GetColor(color);
	Uint8 R = RGBA[0], G = RGBA[1], B = RGBA[2], A = RGBA[3];

	//Draw
	SDL_SetRenderDrawColor(renderer, R, G, B, A);
	SDL_RenderDrawLine(renderer, x1, y1, x2, y2);

	Py_RETURN_NONE;
}

//Function Button(text, x, y, width, height, textcolor, normal, hover, clicked, font = "load(editable)!")
static PyObject *Button(PyObject *self, PyObject *args, PyObject *kwargs)
{
	const char *text;
	int x, y, width, height;
	PyObject *text_color, *normal_color, *hover_color, *clicked_color;
	PyObject *callback = nullptr;
	const char *font;

	static const char *kwlist[] = {"text", "x", "y", "width", "height", "text_color", "normal_color", "hover_color", "clicked_color", "callback", "font", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwargs,  "siiiiOOOOOs", (char **) kwlist, &text, &x, &y, &width, &height, &text_color, &normal_color, &hover_color, &clicked_color, &callback, &font))
	{
		PyErr_SetString(PyExc_TypeError, "Expected: text(str), x(int), y(int), w(int), h(int), text_color(list), normal_color(list), hover_color(list), clicked_color(list), callback(func), font");
		
		return NULL;
	}

	// Validate callback
	if (!PyCallable_Check(callback))
	{
		PyErr_SetString(PyExc_TypeError, "Callback must be a callable function");
		
		return NULL;
	}

	// Load font
	TTF_Font *FONT = TTF_OpenFont(font, height * 0.325);
	if (!FONT)
	{
		PyErr_SetString(PyExc_RuntimeError, "Failed to load font");
		
		return NULL;
	}

	// Convert colors
	vector<Uint8> TextRGBA = GetColor(text_color);
	vector<Uint8> NormalRGBA = GetColor(normal_color);
	vector<Uint8> HoverRGBA = GetColor(hover_color);
	vector<Uint8> PressedRGBA = GetColor(clicked_color);

	COLOR TextColor = {TextRGBA[0], TextRGBA[1], TextRGBA[2], TextRGBA[3]};
	COLOR NormalColor = {NormalRGBA[0], NormalRGBA[1], NormalRGBA[2], NormalRGBA[3]};
	COLOR HoverColor  = {HoverRGBA[0], HoverRGBA[1], HoverRGBA[2], HoverRGBA[3]};
	COLOR PressedColor = {PressedRGBA[0], PressedRGBA[1], PressedRGBA[2], PressedRGBA[3]};

	VECTOR4 region = {x, y, width, height};

	// If pressed: call Python callback
	bool isPressed = button(renderer, NormalColor, HoverColor, PressedColor, region, text, TextColor, FONT);
	if (isPressed) {
		PyObject *result = PyObject_CallObject(callback, NULL);
		if (!result)
			return NULL;
		Py_DECREF(result);
	}

	Py_RETURN_NONE;
}

//Function KeyPressed(event), returns true if that event is pressed. Use like 'if (GUI.KeyPressed("SPACE")):'.
static PyObject *KeyPressed(PyObject *self, PyObject *args)
{
	const char *KeyName;

	if (!PyArg_ParseTuple(args, "s", &KeyName))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : key(string)");
		
		return NULL;
	}

	auto it = keymap.find(KeyName);
	if (it == keymap.end())
	{
		PyErr_SetString(PyExc_ValueError, "Unknown key name.");
		
		return NULL;
	}
	const Uint8 *state = SDL_GetKeyboardState(NULL);
	SDL_Scancode scancode = it->second;

	while (state[scancode])
	{
		return Py_BuildValue("b", true);
	}
	return Py_BuildValue("b", false);
}

//Function MousePressed(KEY), trueif the given key on mouse had been pressed.
static PyObject *MousePressed(PyObject *self, PyObject *args)
{
    const char *buttonName;

    if (!PyArg_ParseTuple(args, "s", &buttonName))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments: button(string)");
        
        return NULL;
    }

    string Button = buttonName;

    if (mousemap.find(Button) == mousemap.end())
    {
        PyErr_SetString(PyExc_ValueError, "Invalid mouse button name");
        
        return NULL;
    }

    int x, y;
    Uint32 buttons = SDL_GetMouseState(&x, &y);
    bool pressed = buttons & SDL_BUTTON(mousemap[Button]);

    return Py_BuildValue("b", pressed);
}

//Function GetMousePos(XorY), returns mouse's x/y pos as per mentioned.
static PyObject *GetMousePos(PyObject *self, PyObject *args)
{
    const char *XorY;

    // Parse the input argument as a string
    if (!PyArg_ParseTuple(args, "s", &XorY))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments: XorY (string)");
        
        return NULL;
    }

    // Get the mouse position using SDL
    int x, y;
    SDL_GetMouseState(&x, &y);

    // Compare strings properly using strcmp
    if (strcmp(XorY, "x") == 0)
    {
        return Py_BuildValue("i", x);
    }
    else if (strcmp(XorY, "y") == 0)
    {
        return Py_BuildValue("i", y);
    }
    else
    {
        PyErr_SetString(PyExc_ValueError, "Use 'x' for X position or 'y' for Y position.");
        
        return NULL;
    }
}

//Function CenterX(width), makes rect, square's x to center
static PyObject *CenterX(PyObject *self, PyObject *args)
{
	int width;

	if (!PyArg_ParseTuple(args, "i", &width))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : width(int)");
		
		return NULL;
	}

	return Py_BuildValue("i", (geometry_x - width)/2);
}

//Function CenterY(height), cener's the y position of a rectangle/square.
static PyObject *CenterY(PyObject *self, PyObject *args)
{
	int height;

	if (!PyArg_ParseTuple(args, "i", &height))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : height(int)");

		return NULL;
	}

	return Py_BuildValue("i", (geometry_y - height)/2);
}

//Function CenterTextX(text, size), centers a text.
static PyObject *CenterTextX(PyObject *self, PyObject *args)
{
	const char *text;
	int size;
	const char *font;

	if(!PyArg_ParseTuple(args, "sis", &text, &size, &font))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : text(string), size(int), font(string)");

		return NULL;
	}

	TTF_Font *FONT= TTF_OpenFont(font, size);

	TTF_SizeText(FONT, text, &size, nullptr);

	return Py_BuildValue("i", (geometry_x - size)/2);
}

//Function LoadIMG(image), to load an image, IMPORTANT : Use this outside of the mainloop.
static PyObject *LoadIMG(PyObject *self, PyObject *args)
{
    const char *name;
    const char *image;

    if (!PyArg_ParseTuple(args, "ss", &name, &image))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments: name(string), image(string)");
        
        return NULL;
    }

    // Load image surface
    SDL_Surface *surface = IMG_Load(image);
    if (!surface) {
        PyErr_SetString(PyExc_RuntimeError, IMG_GetError());
        
        return NULL;
    }

    // Convert to texture
    SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, surface);
    
    SDL_FreeSurface(surface);
    
    if (!texture) {
        PyErr_SetString(PyExc_RuntimeError, SDL_GetError());
        
        return NULL;
    }

    // Store the texture
    images[name] = texture;

    Py_RETURN_NONE;
}

//Function Img(imageFile, x, y, width, height), function to load images.
static PyObject *Img(PyObject *self, PyObject *args, PyObject *kwargs)
{
    const char *name;
    int x, y, width, height;

    static const char *kwlist[] = {"name", "x", "y", "width", "height", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "siiii", (char **)kwlist, &name, &x, &y, &width, &height))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments: name(str), x(int), y(int), width(int), height(int)");
        
        return NULL;
    }

    // Check if image exists
    auto it = images.find(name);
    if (it == images.end())
    {
        PyErr_SetString(PyExc_ValueError, "Image not loaded. Use LoadIMG(name, image) first.");
        
        return NULL;
    }

    SDL_Rect rect = {x, y, width, height};
    SDL_RenderCopy(renderer, it->second, NULL, &rect);

	//Returns x, y, width, height, so that it is easier for the user to use check collusion.
	PyObject *rectangle = PyList_New(4);
	if (!rectangle)
	{
		PyErr_SetString(PyExc_RuntimeError, "Unable to return value.");

		return NULL;
	}

	//setup the variables to add into the list
	PyObject *xObj = PyLong_FromLong(x);
	PyObject *yObj = PyLong_FromLong(y);
	PyObject *widthObj = PyLong_FromLong(width);
	PyObject *heightObj = PyLong_FromLong(height);

	//append to the list
	PyList_SET_ITEM(rectangle, 0, xObj);
	PyList_SET_ITEM(rectangle, 1, yObj);
	PyList_SET_ITEM(rectangle, 2, widthObj);
	PyList_SET_ITEM(rectangle, 3, heightObj);

	return Py_BuildValue("O", rectangle);
}

//Function LoadMusic(name, music), function to load music, IMPORTENT : Use outside the mainloop.
static PyObject *LoadMusic(PyObject *self, PyObject *args)
{
    const char *name;
    const char *music;

    if (!PyArg_ParseTuple(args, "ss", &name, &music))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments: name(string), music(string)");
        return NULL;
    }

    // Check if audio device is initialized
    if (!Mix_QuerySpec(NULL, NULL, NULL))
    {
        PyErr_SetString(PyExc_RuntimeError, "Audio device not initialized. Call InitAudioDevice() first");
        return NULL;
    }

    // Load music file
    Mix_Music *MUS = Mix_LoadMUS(music);
    if (!MUS)
    {
        PyErr_SetString(PyExc_RuntimeError, Mix_GetError());
        
        return NULL;
    }

    // If music with this name already exists, free it first
    auto it = musics.find(name);
    if (it != musics.end())
    {
        Mix_FreeMusic(it->second);
    }

    // Store the music
    musics[name] = MUS;

    Py_RETURN_NONE;
}

//Function LoadBGM(name, bgm), Function to load BGM(sound effects), IMPORTENT : Do not use inside the mainloop.
static PyObject *LoadBGM(PyObject *self, PyObject *args)
{
    const char *name; 
    const char *bgm;

    if (!PyArg_ParseTuple(args, "ss", &name, &bgm))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments: name(string), bgm(string)");
        
        return NULL;
    }

    // Check if audio device is initialized
    if (!Mix_QuerySpec(NULL, NULL, NULL))
    {
        PyErr_SetString(PyExc_RuntimeError, "Audio device not initialized. Call InitAudioDevice() first");
        return NULL;
    }

    Mix_Chunk *BGM = Mix_LoadWAV(bgm);
    if (!BGM)
    {
        PyErr_SetString(PyExc_RuntimeError, Mix_GetError());
        return NULL;
    }

    // Free existing BGM if it exists
    auto it = bgmS.find(name);
    if (it != bgmS.end())
    {
        Mix_FreeChunk(it->second);
    }

    // Store the BGM
    bgmS[name] = BGM;

    Py_RETURN_NONE;
}

//Function PlayMusic(name, times), function to play music.
static PyObject *PlayMusic(PyObject *self, PyObject *args)
{
    const char *name;
    int loop;

    if (!PyArg_ParseTuple(args, "si", &name, &loop))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments: name(string), loop(int)(-1 : unlimited!)");
        return NULL;
    }

    // Check if audio device is initialized
    if (!Mix_QuerySpec(NULL, NULL, NULL))
    {
        PyErr_SetString(PyExc_RuntimeError, "Audio device not initialized");
        return NULL;
    }

    auto it = musics.find(name);
    if (it == musics.end())
    {
        PyErr_SetString(PyExc_ValueError, "Music not loaded. Use LoadMusic(name, music) first");
        return NULL;
    }

    // Stop any currently playing music
    Mix_HaltMusic();
    
    // Play the music
    if (Mix_PlayMusic(it->second, loop) == -1)
    {
        PyErr_SetString(PyExc_RuntimeError, Mix_GetError());
        
        return NULL;
    }

    Py_RETURN_NONE;
}

//Function PlayBGM(name), Function to play bgm.
static PyObject *PlayBGM(PyObject *self, PyObject *args)
{
    const char *name; 
    int loop;

    if (!PyArg_ParseTuple(args, "si", &name, &loop))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments: name(string), loop(int)(0: one time)");
        return NULL;
    }

    // Check if audio device is initialized
    if (!Mix_QuerySpec(NULL, NULL, NULL))
    {
        PyErr_SetString(PyExc_RuntimeError, "Audio device not initialized");
        return NULL;
    }

    // Find the BGM
    auto it = bgmS.find(name);
    if (it == bgmS.end() || !it->second)
    {
        PyErr_SetString(PyExc_ValueError, "BGM not found or invalid. Use LoadBGM(name, bgm) first");
        return NULL;
    }

    // Play the BGM
    if (Mix_PlayChannel(-1, it->second, loop) == -1)
    {
        PyErr_SetString(PyExc_RuntimeError, Mix_GetError());
        return NULL;
    }

    Py_RETURN_NONE;
}

//Function SetLogo(logo), set the window logo.
static PyObject *SetLogo(PyObject *self, PyObject *args)
{
	const char *logo;

	if (!PyArg_ParseTuple(args, "s", &logo))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : logo(string(png : recomeded!)");

		return NULL;
	}

	//Load image
	SDL_Surface *icon = IMG_Load(logo);

	//Set icon
	if (icon)
	{
		SDL_SetWindowIcon(window, icon);
		SDL_FreeSurface(icon);
	}
	else
	{
		PyErr_SetString(PyExc_FileNotFoundError, "No icon file found.");

		return NULL;
	}

	Py_RETURN_NONE;
}

//Function CheckCollisionRect(rectangle1, rectangle2), returns true if both touches.
static PyObject *CheckCollisionRect(PyObject *self, PyObject *args)
{
	PyObject *rect1, *rect2;

	if (!PyArg_ParseTuple(args, "OO", &rect1, &rect2))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : rect1, rect2 (list/rectangle)");

		return NULL;
	}

	//extract x1, y1, w1, h1, x2, y2, w2, h2
	int x1, y1, w1, h1, x2, y2, w2, h2;
	float dummy;
	ExtractFromList(x1, y1, w1, h1, dummy, rect1);
	ExtractFromList(x2, y2, w2, h2, dummy, rect2);

	//check collusion
	bool Collusion = (
		x1 < x2 + w2 &&
		x1 + w1 > x2 &&
		y1 < y2 + h2 &&
		y1 + h1 > y2
	);

	return Py_BuildValue("b", Collusion);
}

//Function CheckCollisionCircle(circle1, circle2). Returns true if circle 1 touches circle 2.
static PyObject *CheckCollisionCircle(PyObject *self, PyObject *args)
{
	PyObject *circle1, *circle2;

	if (!PyArg_ParseTuple(args, "OO", &circle1, &circle2))
	{
		PyErr_SetString(PyExc_TypeError, "Expected arguments : circle1, circle2 (list/circle)");

		return NULL;
	}

	//extract the x1, y1, rad1, x2, y2, rad2
	int x1, y1, x2, y2;
	float rad1, rad2;
	int dummy;
	ExtractFromList(x1, y1, dummy, dummy, rad1, circle1);
	ExtractFromList(x2, y2, dummy, dummy, rad2, circle2);

	bool collusion = (sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2)) < (rad1 + rad2));

	return Py_BuildValue("b", collusion);
}

//Function CheckCollisionRectCircle(rectangle, circle), returns true if the given rectangle and the circle collides each other
static PyObject *CheckCollisionRectCircle(PyObject *self, PyObject *args)
{
    PyObject *rectangle, *circle;

    if (!PyArg_ParseTuple(args, "OO", &rectangle, &circle))
    {
        PyErr_SetString(PyExc_TypeError, "Expected arguments : rectangle, circle (list)");
        return NULL;
    }

    //Extract rectangle properties: x1, y1, width, height
    int x1 = 0, y1 = 0, width = 0, height = 0, DummyWidthOrHeightForCircle;
    float DummyRadForRectangle;
    ExtractFromList(x1, y1, width, height, DummyRadForRectangle, rectangle);

    //Extract circle properties: x2, y2, rad
    //Extract circle properties: x2, y2, rad
	int x2 = 0, y2 = 0;
	float rad = 0.0f;
	if (!PyList_Check(circle) || PyList_Size(circle) != 3) {
		PyErr_SetString(PyExc_TypeError, "Expected circle argument to be a list of size 3 (x, y, radius)");
		return NULL;
	}
	PyObject *x_obj = PyList_GetItem(circle, 0);
	PyObject *y_obj = PyList_GetItem(circle, 1);
	PyObject *rad_obj = PyList_GetItem(circle, 2);

	x2 = PyLong_AsLong(x_obj);
	y2 = PyLong_AsLong(y_obj);
	rad = (float)PyFloat_AsDouble(rad_obj);

	if (PyErr_Occurred()) {
		return NULL;
	}

    //check collusion
    bool collusion = false;

    // Find the closest point on the rectangle to the center of the circle
    float closestX = std::max((float)x1, std::min((float)x2, (float)x1 + width));
    float closestY = std::max((float)y1, std::min((float)y2, (float)y1 + height));

    // Calculate the squared distance between the closest point and the circle's center
    float distanceSq = pow((float)x2 - closestX, 2) + pow((float)y2 - closestY, 2);

    // Check if the squared distance is less than the radius squared
    collusion = distanceSq < (rad * rad);

    return Py_BuildValue("b", collusion);
}

//--functions of GladUI over here, next is about to let understand this C++ to Py--
static PyMethodDef GladUIMethods[] = {
	{"version", version, METH_VARARGS, "Returns the version of GladUI."},
	{"InitAudioDevice", InitAudioDevice, METH_VARARGS, "To Initilize the audio device."},
	{"Mainloop", Mainloop, METH_VARARGS, "Function for mainloop."},
	{"SetFPS", SetFPS, METH_VARARGS, "Set fps as given value."},
	{"GetFPS", GetFPS, METH_VARARGS, "Returns current FPS."},
	{"CreateWindow", (PyCFunction)CreateWindow, METH_VARARGS | METH_KEYWORDS, "Create window."},
	{"START", START, METH_VARARGS, "Shows the bg."},
	{"END", END, METH_VARARGS, "Present the renderer."},
	{"SetAutoCloseFalse", SetAutoCloseFalse, METH_VARARGS,"Set automatically closing while close button is pressed to false."},
	{"QuitMessage", QuitMessage, METH_VARARGS, "Returns true while close button is pressed."},
	{"Quit", Quit, METH_VARARGS, "Breaks the mainloop."},
	{"DrawText", (PyCFunction)DrawText, METH_VARARGS | METH_KEYWORDS, "Draws a text on the screen."},
	{"Rect", (PyCFunction)Rect, METH_VARARGS|METH_KEYWORDS, "Draws a rectangle on the screen."},
	{"Circle", (PyCFunction)Circle, METH_VARARGS | METH_KEYWORDS, "Draws a circle on the screen."},
	{"Point", Point, METH_VARARGS, "Draws a point at the given position."},
	{"Line", Line, METH_VARARGS, "Draws a line from (x1, y1) to (x2, y2)."},
	{"Button", (PyCFunction)Button, METH_VARARGS | METH_KEYWORDS, "Add a button on the screen."},
	{"KeyPressed", KeyPressed, METH_VARARGS, "Returns true if key on event had pressed."},
	{"MousePressed", MousePressed, METH_VARARGS, "Returns true if the given event had been pressed on mouse."},
	{"GetMousePos", GetMousePos, METH_VARARGS, "Returns mouse x/y position."},
	{"CenterX", CenterX, METH_VARARGS, "Centers the x position of a rectangle/square."},
	{"CenterY", CenterY, METH_VARARGS, "Centers the y position of a rectangle/square."},
	{"CenterTextX", CenterTextX, METH_VARARGS, "Center the x position of a text."},
	{"LoadIMG", LoadIMG, METH_VARARGS, "To load image."},
	{"Img", (PyCFunction)Img, METH_VARARGS | METH_KEYWORDS, "To show image."},
	{"LoadMusic", LoadMusic, METH_VARARGS, "Function to load music."},
	{"LoadBGM", LoadBGM, METH_VARARGS, "Function to load BGM's."},
	{"PlayMusic", PlayMusic, METH_VARARGS, "Function to play music."},
	{"PlayBGM", PlayBGM, METH_VARARGS, "Function to play BGM."},
	{"SetLogo", SetLogo, METH_VARARGS, "Function to set the window logo."},
	{"CheckCollisionRect", CheckCollisionRect, METH_VARARGS, "Returns true if rectangle1 and rectangle2 collide with each other."},
	{"CheckCollisionCircle", CheckCollisionCircle, METH_VARARGS, "Returns true if circle 1 and circle 2 collide with each other."},
	{"CheckCollisionRectCircle", CheckCollisionRectCircle, METH_VARARGS, "Returns true if the rectangle and the circle collide with each other."},
    
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef gladuimodule = {
    PyModuleDef_HEAD_INIT,
    "GladUI",       
    NULL, 
    -1,            
    GladUIMethods
};

PyMODINIT_FUNC PyInit_GladUI(void)
{
    return PyModule_Create(&gladuimodule);
}
