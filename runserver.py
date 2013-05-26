def run(host, port):
    from application import app
    app.run(debug=True)

if __name__ == '__main__':
    run(host='localhost', port=5000)
