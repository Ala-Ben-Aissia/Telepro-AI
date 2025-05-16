import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Define routes that require authentication
const protectedRoutes = [
  "/patients",
  "/patient",
  "/campaigns",
  "/segments",
  "/dashboard",
];

// Define routes that are always public
const publicRoutes = [
  "/auth/login",
  "/auth/register",
  "/favicon.ico",
];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const accessToken = request.cookies.get("accessToken")?.value;

  // Allow all API routes and static files
  if (
    pathname.startsWith("/api") ||
    pathname.startsWith("/_next") ||
    pathname.startsWith("/static")
  ) {
    return NextResponse.next();
  }

  // If user is authenticated and tries to access login or register, redirect to dashboard
  if (
    (pathname.startsWith("/auth/login") ||
      pathname.startsWith("/auth/register")) &&
    accessToken
  ) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // Allow public routes
  if (publicRoutes.some(route => pathname.startsWith(route))) {
    return NextResponse.next();
  }

  // Check if the route is protected
  if (protectedRoutes.some(route => pathname.startsWith(route))) {
    if (!accessToken) {
      const loginUrl = new URL("/auth/login", request.url);
      // loginUrl.searchParams.set('next', pathname)
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/patients/:path*",
    "/patient/:path*",
    "/campaigns/:path*",
    "/segments/:path*",
    "/dashboard/:path*",
    "/auth/login",
    "/auth/register",
    "/favicon.ico",
    "/api/:path*",
  ],
};
