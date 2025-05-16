import { ReactNode } from "react";

export default function PatientLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div>
      <main className="container mx-auto p-4 pt-24">{children}</main>
    </div>
  );
}
