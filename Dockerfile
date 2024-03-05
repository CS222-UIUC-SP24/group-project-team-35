FROM python
WORKDIR /
COPY . .
RUN pip install -r requirements.txt
ENV SPOTIPY_CLIENT_ID b0203c1f3cea49668da16b6c09cb753d
ENV SPOTIPY_CLIENT_SECRET 08b6826a5f584a9ebd6d1cec2414656e
ENV SPOTIPY_REDIRECT_URI http://localhost:8000
# can expose other ports as needed
EXPOSE 8000
# assuming we name our entrypoint app.py
CMD ["python3", "app.py"]
