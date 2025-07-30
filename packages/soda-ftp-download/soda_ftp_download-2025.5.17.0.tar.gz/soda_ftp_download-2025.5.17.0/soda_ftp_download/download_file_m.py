import ftplib
import os


def is_jupyter():
    try:
        __IPYTHON__  # type: ignore
        return True
    except NameError:
        return False


ftp_user = "anonymous"
ftp_password = ""


def download_file(url: str, local_file: str = ""):
    if is_jupyter():
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm
    if not url.startswith("ftp://"):
        print("incorrect url")
        return

    url_no_ftp = url[len("ftp://") :]
    ftp_host = url_no_ftp[: url_no_ftp.index("/")]
    remote_file = url_no_ftp[url_no_ftp.index("/") :]

    if local_file == "":
        local_file = url_no_ftp[url_no_ftp.rfind("/") + 1 :]
    try:
        with ftplib.FTP(ftp_host) as ftp:
            ftp.login(ftp_user, ftp_password)

            try:
                file_size = ftp.size(remote_file)
            except ftplib.error_perm as e:
                if "550" in str(e):
                    print(
                        "Warning: Could not determine remote file size. Progress might not be accurate."
                    )
                    file_size = None
                else:
                    raise

            rest_position = 0
            if os.path.exists(local_file):
                rest_position = os.path.getsize(local_file)
                # print(rest_position, file_size)
                if rest_position == file_size:
                    print("file already downloaded")
                    return
                print(f"Resuming download from byte: {rest_position}")
                ftp.sendcmd(f"REST {rest_position}")

            with open(local_file, "ab") as lf:
                if file_size is not None:
                    pbar = tqdm(
                        total=file_size,
                        initial=rest_position,
                        unit="B",
                        unit_scale=True,
                        desc=local_file,
                    )
                else:
                    pbar = tqdm(
                        unit="B", unit_scale=True, desc=local_file
                    )  # Without total size

                def callback(data):
                    lf.write(data)
                    pbar.update(len(data))

                ftp.retrbinary(f"RETR {remote_file}", callback)

                pbar.close()
                print("Download complete!")

    except ftplib.all_errors as e:
        print(f"FTP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
