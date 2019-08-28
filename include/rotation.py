import numpy as np

def getRotationMatrix(gravity, geomagnetic):

	""" 
	Python implementation of the getRotationMatrix method from Android's API, as presented in

	https://android.googlesource.com/platform/frameworks/base/+/master/core/java/android/hardware/SensorManager.java
	"""

	Ax = gravity[0]
	Ay = gravity[1]
	Az = gravity[2]
	normsqA = (Ax * Ax + Ay * Ay + Az * Az)
	g = 9.81
	freeFallGravitySquared = 0.01 * g * g

	if normsqA < freeFallGravitySquared:
		# gravity less than 10% of normal value
		return False

	Ex = geomagnetic[0]
	Ey = geomagnetic[1]
	Ez = geomagnetic[2]
	Hx = Ey * Az - Ez * Ay
	Hy = Ez * Ax - Ex * Az
	Hz = Ex * Ay - Ey * Ax

	normH = np.sqrt(Hx * Hx + Hy * Hy + Hz * Hz)

	if normH < 0.1:
		# device is close to free fall (or in space?), or close to
		# magnetic north pole. Typical values are  > 100.
		return False

	invH = 1.0 / normH
	Hx *= invH
	Hy *= invH
	Hz *= invH

	invA = 1.0 / np.sqrt(Ax * Ax + Ay * Ay + Az * Az)
	Ax *= invA
	Ay *= invA
	Az *= invA

	Mx = Ay * Hz - Az * Hy
	My = Az * Hx - Ax * Hz
	Mz = Ax * Hy - Ay * Hx

	R = np.zeros(9)

	R[0] = Hx;     R[1] = Hy;     R[2] = Hz
	R[3] = Mx;     R[4] = My;     R[5] = Mz
	R[6] = Ax;     R[7] = Ay;     R[8] = Az

	# R = np.zeros(16)
	# R[0]  = Hx;    R[1]  = Hy;    R[2]  = Hz;   R[3]  = 0
	# R[4]  = Mx;    R[5]  = My;    R[6]  = Mz;   R[7]  = 0
	# R[8]  = Ax;    R[9]  = Ay;    R[10] = Az;   R[11] = 0
	# R[12] = 0;     R[13] = 0;     R[14] = 0;    R[15] = 1

	invE = 1.0 / np.sqrt(Ex * Ex + Ey * Ey + Ez * Ez)
	c = (Ex * Mx + Ey * My + Ez * Mz) * invE
	s = (Ex * Ax + Ey * Ay + Ez * Az) * invE

	I = np.zeros(9)

	I[0] = 1;     I[1] = 0;     I[2] = 0;
	I[3] = 0;     I[4] = c;     I[5] = s;
	I[6] = 0;     I[7] = -s;    I[8] = c;

	# I = np.zeros(16)
	# I[0] = 1;     I[1] = 0;     I[2] = 0;
	# I[4] = 0;     I[5] = c;     I[6] = s;
	# I[8] = 0;     I[9] = -s;     I[10] = c;
	# I[3] = I[7] = I[11] = I[12] = I[13] = I[14] = 0;
	# I[15] = 1;

	return R, I


def getOrientation(R):

	""" 
	Python implementation of the getOrientation method from Android's API, as presented in

	https://android.googlesource.com/platform/frameworks/base/+/master/core/java/android/hardware/SensorManager.java
	"""

	values = np.zeros(3)

	# if len(R) == 9:
	values[0] = np.arctan2(R[1], R[4])
	values[1] = np.arcsin(-R[7])
	values[2] = np.arctan2(-R[6], R[8])
	# elif len(R) == 16:
	# 	values[0] = np.arctan2(R[1], R[5]);
	# 	values[1] = np.arcsin(-R[9]);
	# 	values[2] = np.arctan2(-R[8], R[10]);

	return values 

def get_azimuth(acc_x, acc_y, acc_z, mag_x, mag_y, mag_z, decli):

	azimuth = []
	for i in range(0, len(acc_x)):
		accs=(acc_x[i], acc_y[i], acc_z[i])
		mags=(mag_x[i], mag_y[i], mag_z[i])
		R, I = getRotationMatrix(accs, mags)
		azimuth.append( np.degrees(getOrientation(R)[0]) + decli[i] )

	return azimuth



def reorientation(X,Y,Z, phi=0 ):

	xm = np.median(X)
	ym = np.median(Y)
	zm = np.median(Z)

	g = np.sqrt(xm**2 + ym**2 + zm**2)

	alpha = np.arcsin(xm/g)
	beta  = np.arcsin(ym/g)

	phi *= -1

	ca = np.cos(alpha)
	sa = np.sin(alpha)
	cb = np.cos(beta)
	sb = np.sin(beta)
	cp = np.cos(phi)
	sp = np.sin(phi)

	l = list(map(
		lambda x,y,z: [
			y*cb*sp + z*(-cp*sa -ca*sb*sp) + x*(ca*cp -sa*sb*sp),
			y*cb*cp + x*(-cp*sa*sb -ca*sp) + z*(sa*sp -ca*cp*sb),
			z*ca*cb + x*sa*cb + y*sb
		],
		X,Y,Z
	))

	return np.array(l)	

