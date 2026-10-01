import { useForm } from "react-hook-form";
import { Loader2 } from "lucide-react";

export function Settings({ isLoading, price }: { isLoading: boolean; price: number }) {
  const { register, formState } = useForm({ mode: "onChange" });
  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <Loader2 className="animate-spin" />
      </div>
    );
  }
  return (
    <form className="max-w-md mx-auto p-6 space-y-4">
      <label className="text-sm font-medium">Email *</label>
      <input className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="Email" {...register("email")} />
      <input className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm" type="password" placeholder="Password" {...register("password")} />
      <p className="text-gray-500">Plan: ${price.toFixed(1)} per month</p>
      <button disabled={!formState.isValid} className="w-full rounded-md bg-indigo-600 py-2 text-white">Save</button>
      <button type="button" className="text-sm">Reset password</button>
    </form>
  );
}
