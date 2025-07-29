use std::{
    sync::{mpsc, Arc, Mutex},
    thread::{spawn, JoinHandle},
};

type Task = Box<dyn FnOnce() + Send + 'static>;

pub struct ThreadPool {
    _workers: Vec<Worker>,
    task_tx: mpsc::Sender<Option<Task>>,
    sync_rx: mpsc::Receiver<()>,
}

impl ThreadPool {
    pub fn new(n: usize) -> Self {
        assert!(n > 0);

        let (task_tx, task_rx) = mpsc::channel();
        let task_rx = Arc::new(Mutex::new(task_rx));

        let (sync_tx, sync_rx) = mpsc::channel();

        let mut workers = Vec::with_capacity(n);

        for _ in 0..n {
            workers.push(Worker::new(Arc::clone(&task_rx), sync_tx.clone()));
        }

        Self {
            _workers: workers,
            task_tx,
            sync_rx,
        }
    }

    pub fn run<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        self.task_tx.send(Some(job)).unwrap();
    }

    pub fn sync(&self) {
        // Send a sync point to job channel
        self.task_tx.send(None).unwrap();
        // When the sync point is reached, the worker will send a confirmation to the sync channel
        // Block until the confirmation is received
        let _ = self.sync_rx.recv().unwrap();
    }
}

struct Worker {
    _thread: JoinHandle<()>,
}

impl Worker {
    fn new(task_rx: Arc<Mutex<mpsc::Receiver<Option<Task>>>>, sync_tx: mpsc::Sender<()>) -> Worker {
        let thread = spawn(move || loop {
            let task = task_rx.lock().unwrap().recv();
            match task {
                Ok(Some(job)) => {
                    job();
                }
                Ok(None) => {
                    sync_tx.send(()).unwrap();
                }
                Err(_) => break,
            }
        });

        Worker { _thread: thread }
    }
}
