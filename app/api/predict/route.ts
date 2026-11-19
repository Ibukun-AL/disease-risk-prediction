import { NextResponse } from "next/server";
import { predict, validateFeatures } from "@/lib/predict";

export async function POST(req: Request) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Send a JSON body." }, { status: 400 });
  }
  const v = validateFeatures((body as { features?: unknown } | null)?.features);
  if (!v.ok) return NextResponse.json({ error: v.error }, { status: 422 });
  return NextResponse.json(predict(v.features));
}
