// Meta-Analysis Audit — desktop shell.
//
// The shell's only job is supervision: start the local Python backend
// (API + worker) with its data directory in the platform app-data location,
// show the UI, and shut the backend down with the window. The researcher
// never starts a server or sees a terminal (doc 00 A1).

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::path::{Path, PathBuf};
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::time::{Duration, Instant};

use tauri::{Manager, RunEvent};

const API_PORT: u16 = 8977;

struct Backend(Mutex<Option<Child>>);

fn backend_dir() -> PathBuf {
    if let Ok(dir) = std::env::var("METAAUDIT_BACKEND_DIR") {
        return PathBuf::from(dir);
    }
    // Development layout: <repo>/src-tauri + <repo>/backend.
    // A packaged build will ship the backend as a bundled sidecar and set
    // METAAUDIT_BACKEND_DIR via the bundle resources (packaging track).
    Path::new(env!("CARGO_MANIFEST_DIR")).join("../backend")
}

fn spawn_backend(data_dir: &Path) -> std::io::Result<Child> {
    let backend = backend_dir();
    let python = backend.join(".venv/bin/python");
    Command::new(python)
        .current_dir(&backend)
        .args([
            "-m",
            "uvicorn",
            "app.api.main:create_app",
            "--factory",
            "--host",
            "127.0.0.1",
            "--port",
            &API_PORT.to_string(),
        ])
        .env("METAAUDIT_DATA_DIR", data_dir)
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
}

fn wait_for_api(timeout: Duration) -> bool {
    let deadline = Instant::now() + timeout;
    while Instant::now() < deadline {
        if std::net::TcpStream::connect(("127.0.0.1", API_PORT)).is_ok() {
            return true;
        }
        std::thread::sleep(Duration::from_millis(150));
    }
    false
}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let data_dir = app
                .path()
                .app_data_dir()
                .expect("could not resolve app data directory");
            std::fs::create_dir_all(&data_dir).ok();

            let child = spawn_backend(&data_dir)
                .map_err(|e| format!("failed to start local backend: {e}"))?;
            app.manage(Backend(Mutex::new(Some(child))));
            wait_for_api(Duration::from_secs(15));
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while building the application")
        .run(|app, event| {
            if let RunEvent::Exit = event {
                if let Some(backend) = app.try_state::<Backend>() {
                    if let Some(mut child) = backend.0.lock().unwrap().take() {
                        let _ = child.kill();
                        let _ = child.wait();
                    }
                }
            }
        });
}
