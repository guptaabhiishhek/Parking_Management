# Parking_Management
# 🚗 Smart Parking Space Detector with PostgreSQL Integration
An AI-powered, real-time Computer Vision system that detects parking space occupancy from video feeds and logs entry/exit data into a PostgreSQL database.
Built with **Python**, **OpenCV**, **cvzone**, and **PostgreSQL**, this application provides a complete end-to-end pipeline: from interactive visual parking space mapping to real-time image processing, occupancy detection, and database auditing.
---
## 🌟 Key Features
*   **Interactive Parking Slot Selector (`ParkingSpacePicker.py`):** An intuitive GUI tool to visually map and save parking slots. Define parking slot coordinates with a simple **Left-Click** and remove them using **Right-Click**. Bounding boxes are automatically serialized and loaded.
*   **Real-Time Occupancy Analytics (`main.py`):** Uses advanced image processing techniques (Gaussian Blur, Adaptive Thresholding, Median Filtering, and Dilation) to detect whether a car is occupying a specific marked slot in real-time.
*   **Live UI HUD Overlay:** Displays a live counter on the video stream showing available vs. total parking spaces (e.g., `Free: 12/69`) with active color-coded visual indicator boxes (**Green** for free, **Red** for occupied).
*   **PostgreSQL Relational Logging:** Automatically connects to a database and inserts a record when a space is filled or vacated, keeping a clean log of vehicle IDs, entry timestamps, exit timestamps, and total parking duration.
---
## 🛠️ Tech Stack & Dependencies
*   **Language:** Python 3.x
*   **Computer Vision:** OpenCV (`opencv-python`)
*   **GUI Helpers:** `cvzone` (custom text overlay and shapes)
*   **Data Processing:** NumPy (matrix masking)
*   **Database Connector:** `psycopg2` or `psycopg2-binary` (PostgreSQL adapter)
*   **Object Serialization:** Python's native `pickle` (for saving box coordinates)
*   **Database:** PostgreSQL (Relational DBMS)
---
## 📐 Project Structure
```bash
ParkingProject/
│
├── ParkingProject/
│   ├── .idea/                 # IDE Configuration files
│   ├── venv/                  # Virtual Environment
│   ├── carPark.mp4            # Input video feed of the parking lot
│   ├── carParkImg.png         # Reference image used for defining slot positions
│   ├── CarParkPos             # Pickle file containing serialized slot coordinates (x, y)
│   ├── main.py                # Main real-time computer vision & DB logging script
│   └── ParkingSpacePicker.py  # Utility script to define/delete slot coordinates
│
└── README.md                  # This documentation file
```
---
## 🔌 Database Setup (PostgreSQL)
Before running `main.py`, you need to set up your PostgreSQL server and table structure.
1. Create a database named `parking_db`:
   ```sql
   CREATE DATABASE parking_db;
   ```
2. Connect to the `parking_db` database and create the `parked_vehicles` table:
   ```sql
   CREATE TABLE parked_vehicles (
       id SERIAL PRIMARY KEY,
       vehicle_id VARCHAR(50) NOT NULL,
       entry_time TIMESTAMP NOT NULL,
       exit_time TIMESTAMP,
       parking_duration INTERVAL
   );
   ```
3. Update the database credentials inside `main.py` (lines 10-16) if your configuration differs:
   ```python
   conn = psycopg2.connect(
       dbname="parking_db",
       user="postgres",
       password="your_password",  # Default is 'sql' in code
       host="localhost",
       port="5432"
   )
   ```
---
## 🚀 Installation & Quick Start
### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ParkingProject.git
cd ParkingProject/ParkingProject
```
### 2. Set Up Virtual Environment & Dependencies
We recommend using Python's virtual environment:
```bash
# Create virtual environment
python -m venv venv
# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
# Install required packages
pip install opencv-python numpy cvzone psycopg2-binary
```
### 3. Step 1: Define Parking Spaces (`ParkingSpacePicker.py`)
Run the space picker tool to draw or adjust the bounding boxes for each parking space in the parking lot:
```bash
python ParkingSpacePicker.py
```
*   **To Add a Space:** Click the **Left Mouse Button** at the top-left corner of any empty parking spot.
*   **To Remove a Space:** Click the **Right Mouse Button** inside any existing magenta box.
*   Close the window when you are done; coordinates are automatically pickled and saved to `CarParkPos`.
### 4. Step 2: Run Real-time Detection (`main.py`)
Ensure your PostgreSQL database is running and start the detector:
```bash
python main.py
```
*   The script will load the video feed `carPark.mp4`.
*   Empty slots will highlight in **Green (Thick borders)** and occupied spots in **Red (Thin borders)**.
*   The screen will display a real-time HUD with the count of free spots.
*   Entry and exit transactions will print to the console and automatically save to the PostgreSQL database table.
*   Press **`q`** on your keyboard while focusing on the video window to quit.
---
## 🧠 How It Works (Under the Hood)
1. **Preprocessing Layer:**
   The video stream undergoes frame-by-frame processing. Each frame is converted to grayscale, softened with a Gaussian Blur to remove high-frequency noise, and then transformed into a binary image using **Adaptive Thresholding** to separate parking markings and cars from the asphalt. A median filter is then applied followed by dilation to solidify pixel groupings.
   
2. **Feature Extraction & Pixel Count:**
   For each parking position coordinate saved in `CarParkPos`:
   * The binary threshold image is cropped to the exact size of the slot (`107x48` pixels).
   * `cv2.countNonZero(imgCrop)` counts white pixels (which represent visual noise/features like cars).
   * If the pixel count is below `900`, the spot is classified as **Empty**. If it exceeds `900`, a vehicle is present, and the slot is classified as **Occupied**.
3. **Database Audit Trail:**
   * The program tracks the previous state (`prev_spaceCounter`).
   * When `spaceCounter` decreases, the system recognizes a vehicle has entered, printing an insertion update.
   * When `spaceCounter` increases, the system computes the exact duration the vehicle spent parked and performs an update query.
---
## 🛠️ Customization
You can fine-tune the system parameters at the top of the scripts:
*   **Slot Dimensions:** Adjust `width, height = 107, 48` to match your specific camera angle or parking lot size.
*   **Threshold Value:** In `main.py`, change `count < 900` to make the occupancy detection more or less sensitive.
---
## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
---
*Created with ❤️ using OpenCV & Python.*
