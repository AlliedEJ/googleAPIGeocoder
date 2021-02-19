from flask import Flask, render_template, request, send_file
import geocoder
import pandas

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        try:
            df=pandas.read_csv(request.files["file_name"])
            latlonList=[]
            for i in df["Addresses"]:
                g=geocoder.google(i, key='<<YOUR API KEY HERE>>')
                l=g.latlng
                latlonList.append(l)
            df["LatLon"]=latlonList
            tableView=df.to_html(classes='table table-striped')
            df.to_csv('latlonDataTable.csv')
            return render_template("result.html", table=tableView)
        except:
            return render_template('index.html', text="There was a problem -- the upload must be a csv with 'Addresses' as the column label.")

@app.route("/download")
def download():
    return send_file('latlonDataTable.csv', attachment_filename="yourLatLonFile.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)