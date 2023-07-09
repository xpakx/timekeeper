import type { TimerMin } from "./TimerMin";

export type RunningTimerDetails = {
    id: number;
    start_time: Date;
    end_time?: Date;
    state: String;
    timer_id: number;
    timer: TimerMin;
    reward_time?: number;
}