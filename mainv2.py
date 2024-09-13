import cv2

# Initialize the video capture
cap = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        break
    
    inverted_i = cv2.flip(frame, 1)

    # Display the resulting frame
    cv2.imshow('License Plate Recognition', inverted_i)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
