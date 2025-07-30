/*
  GladG (Advanced helper for SDL usage)
  GladGamingStudio 2025-26

  This software is provided 'as-is', without any express or implied
  warranty. In no event will the authors be held liable for any damages
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

#ifndef GLADG_H
#define GLADG_H

#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h>
#include <string>
#include <functional>
#include <vector>
#include <unordered_map>

using namespace std;

// ---------- DATATYPES ----------

class VECTOR2 {
public:
    int x, y;
};

class VECTOR4 {
public:
    int x, y, width, height;
};

class COLOR {
public:
    Uint8 r, g, b, a;

    COLOR(Uint8 red = 255, Uint8 green = 255, Uint8 blue = 255, Uint8 alpha = 255)
        : r(red), g(green), b(blue), a(alpha) {}

    SDL_Color to_sdl() const {
        return SDL_Color{r, g, b, a};
    }
};

// ---------- AnimationPlayer ----------

class AnimationPlayer {
private:
    unordered_map<string, vector<SDL_Texture*>> tree;
    int FrameIndex = 0;
    bool play_animation = false;

public:
    SDL_Renderer *renderer;
    SDL_Rect object;

    AnimationPlayer(SDL_Renderer *ren, SDL_Rect obj)
        : renderer(ren), object(obj) {}

    void add(string name, vector<string> files) {
        vector<SDL_Texture*> frames;
        for (const auto& file : files) {
            SDL_Surface *surface = IMG_Load(file.c_str());
            SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, surface);
            SDL_FreeSurface(surface);
            frames.push_back(texture);
        }
        tree[name] = frames;
    }

    void play(string name, float delay_seconds = 0.25f) {
        if (play_animation) {
            FrameIndex = (FrameIndex + 1) % tree[name].size();
            SDL_RenderCopy(renderer, tree[name][FrameIndex], NULL, &object);
            SDL_Delay(static_cast<Uint32>(delay_seconds * 1000));
        } else {
            play_animation = true;
        }
    }

    void stop() { play_animation = false; }
};

// ---------- FUNCTIONS ----------

// Get current FPS
inline int getFPS() {
    static Uint32 last_time = 0;
    static int frames = 0;
    static int fps = 0;

    frames++;
    Uint32 now = SDL_GetTicks();
    if (now - last_time >= 1000) {
        fps = frames;
        frames = 0;
        last_time = now;
    }
    return fps;
}

// Cap frame rate
inline void setFPS(int targetFPS) {
    static Uint32 lastFrameTime = 0;
    Uint32 current = SDL_GetTicks();
    Uint32 frameDelay = 1000 / targetFPS;

    if ((current - lastFrameTime) < frameDelay) {
        SDL_Delay(frameDelay - (current - lastFrameTime));
    }

    lastFrameTime = SDL_GetTicks();
}

// Draw text on screen
inline void Drawtext(SDL_Renderer* renderer, const char *fontPath, const char* text, SDL_Color color, VECTOR2 position, int size) {
    TTF_Font *font = TTF_OpenFont(fontPath, size);
    if (!font) return;

    SDL_Surface* surface = TTF_RenderText_Blended(font, text, color);
    if (!surface) {
        TTF_CloseFont(font);
        return;
    }

    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
    if (!texture) {
        SDL_FreeSurface(surface);
        TTF_CloseFont(font);
        return;
    }

    SDL_Rect rect = {position.x, position.y, surface->w, surface->h};
    SDL_RenderCopy(renderer, texture, NULL, &rect);

    SDL_FreeSurface(surface);
    SDL_DestroyTexture(texture);
    TTF_CloseFont(font);
}

// Button
inline bool button(SDL_Renderer* renderer, COLOR normal, COLOR hover, COLOR clicked, VECTOR4 region, const char* text, COLOR textColor, TTF_Font *font) {
    SDL_Rect rect = { region.x, region.y, region.width, region.height };

    int mx, my;
    Uint32 mouse = SDL_GetMouseState(&mx, &my);
    SDL_Point point = { mx, my };

    bool hovering = SDL_PointInRect(&point, &rect);
    bool isDown = (mouse & SDL_BUTTON(SDL_BUTTON_LEFT));
    
    static bool wasDownLastFrame = false;
    bool isClicked = false;

    if (hovering && isDown && !wasDownLastFrame) {
        isClicked = true;  // Only true for one frame on press
    }

    wasDownLastFrame = isDown;

    SDL_Color currentColor = normal.to_sdl();
    if (isDown && hovering)
        currentColor = clicked.to_sdl();
    else if (hovering)
        currentColor = hover.to_sdl();

    // Draw background
    SDL_SetRenderDrawColor(renderer, currentColor.r, currentColor.g, currentColor.b, currentColor.a);
    SDL_RenderFillRect(renderer, &rect);

    // Draw border
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderDrawRect(renderer, &rect);

    // Draw text
    if (font && text) {
        SDL_Color sdlTextColor = textColor.to_sdl();
        SDL_Surface* surface = TTF_RenderText_Blended(font, text, sdlTextColor);
        SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);

        SDL_Rect textRect = {
            region.x + (region.width - surface->w) / 2,
            region.y + (region.height - surface->h) / 2,
            surface->w,
            surface->h
        };

        SDL_RenderCopy(renderer, texture, NULL, &textRect);
        SDL_FreeSurface(surface);
        SDL_DestroyTexture(texture);
    }

    return isClicked;
}

#endif
