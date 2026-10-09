// bbport: host threads that may call guest code (AvPlayer allocator callbacks).
// Each thread gets a guest TCB (GS base, TLS) from the C runtime before running.
#pragma once
#include <atomic>
#include <chrono>
#include <cstdio>
#include <functional>
#include <memory>
#include <stop_token>
#include <system_error>
#include <thread>
#include "common/types.h"

extern "C" void runtime_thread_attach_host(const char* name);

namespace Libraries::Kernel {
class Thread {
public:
    Thread() = default;
    ~Thread() { Stop(); }
    void Run(std::function<void(std::stop_token)>&& func) {
        finished = std::make_shared<std::atomic<bool>>(false);
        thread = std::jthread([func = std::move(func), done = finished](std::stop_token stop) {
            runtime_thread_attach_host("bb:hle");
            func(stop);
            done->store(true);
        });
    }
    // A thread may stop its own Thread object (AvPlayer does); it detaches instead of joining.
    // bbport: these are called from guest code, which a C++ exception cannot unwind: a failed
    // join is logged and the thread detached after a bounded timeout.
    void Join() {
        if (!thread.joinable()) return;
        try {
            if (thread.get_id() == std::this_thread::get_id()) thread.detach();
            else thread.join();
        } catch (const std::system_error& error) {
            std::fprintf(stderr, "HLE thread: join failed (%s); waiting with timeout\n", error.what());
            if (finished) {
                // Wait up to 200ms, then detach so the main thread NEVER deadlocks
                int wait_count = 0;
                while (!finished->load() && wait_count < 200) {
                    std::this_thread::sleep_for(std::chrono::milliseconds(1));
                    wait_count++;
                }
            }
            thread.detach();
        }
    }
    bool Joinable() const { return thread.joinable(); }
    void Stop() {
        if (thread.joinable()) {
            thread.request_stop();
            Join();
        }
    }

private:
    std::jthread thread;
    std::shared_ptr<std::atomic<bool>> finished;
};
} // namespace Libraries::Kernel
